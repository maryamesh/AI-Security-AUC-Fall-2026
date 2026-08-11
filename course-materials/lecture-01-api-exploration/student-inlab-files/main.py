"""Lecture 1 lab: inspect an LLM request and response through FastAPI Swagger."""

from __future__ import annotations

import os
import random
import time
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="Lecture 1: LLM Request Inspector",
    description=(
        "Use POST /chat to inspect message roles, model selection, temperature, "
        "token usage, latency, and generated output. Use POST /compare to run a "
        "controlled temperature comparison."
    ),
    version="1.0.0",
)


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=8_000)


class ChatRequest(BaseModel):
    model: str = Field(default="qwen3:4b", min_length=1)
    messages: list[ChatMessage] = Field(min_length=1, max_length=20)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "qwen3:4b",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Explain concepts to a senior CS student.",
                        },
                        {
                            "role": "user",
                            "content": "Explain how an LLM generates its next token.",
                        },
                    ],
                    "temperature": 0.7,
                }
            ]
        }
    }


class Usage(BaseModel):
    input_tokens: int | None
    output_tokens: int | None
    source: Literal["provider", "approximation", "unavailable"]


class ChatResponse(BaseModel):
    response: str
    model: str
    temperature: float
    finish_reason: str | None
    latency_ms: float
    usage: Usage
    backend: str


class CompareRequest(BaseModel):
    model: str = "qwen3:4b"
    messages: list[ChatMessage] = Field(min_length=1, max_length=20)


class CompareResult(BaseModel):
    temperature: float
    response: str
    latency_ms: float
    usage: Usage


class CompareResponse(BaseModel):
    model: str
    results: list[CompareResult]


def _mock_chat(request: ChatRequest) -> ChatResponse:
    """Offline fallback. Its token counts are word approximations, not real tokens."""
    started = time.perf_counter()
    user_text = next(
        (message.content for message in reversed(request.messages) if message.role == "user"),
        "No user message was supplied.",
    )
    system_text = next(
        (message.content for message in request.messages if message.role == "system"),
        "No system message was supplied.",
    )

    styles = [
        "A language model processes the context and assigns probabilities to possible next tokens.",
        "An LLM repeatedly predicts one token, appends it to the context, and predicts again.",
        "Text generation is an iterative process: tokenize the context, score the next token, select one, and repeat.",
    ]
    style = styles[0] if request.temperature == 0 else random.choice(styles)
    answer = (
        f"{style}\n\n"
        f"Mock observation — system message: {system_text}\n"
        f"Mock observation — user message: {user_text}"
    )
    latency_ms = round((time.perf_counter() - started) * 1_000, 2)
    input_words = sum(len(message.content.split()) for message in request.messages)

    return ChatResponse(
        response=answer,
        model=request.model,
        temperature=request.temperature,
        finish_reason="stop",
        latency_ms=latency_ms,
        usage=Usage(
            input_tokens=input_words,
            output_tokens=len(answer.split()),
            source="approximation",
        ),
        backend="mock",
    )


def _openai_compatible_chat(request: ChatRequest) -> ChatResponse:
    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    if not base_url or not api_key:
        raise HTTPException(
            status_code=500,
            detail="LLM_BASE_URL and LLM_API_KEY must be configured.",
        )

    client = OpenAI(base_url=base_url, api_key=api_key)
    started = time.perf_counter()
    try:
        result = client.chat.completions.create(
            model=request.model,
            messages=[message.model_dump() for message in request.messages],
            temperature=request.temperature,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"The configured LLM backend failed: {type(exc).__name__}",
        ) from exc

    latency_ms = round((time.perf_counter() - started) * 1_000, 2)
    usage = result.usage
    return ChatResponse(
        response=result.choices[0].message.content or "",
        model=result.model,
        temperature=request.temperature,
        finish_reason=result.choices[0].finish_reason,
        latency_ms=latency_ms,
        usage=Usage(
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            source="provider" if usage is not None else "unavailable",
        ),
        backend=os.getenv("LLM_BACKEND", "ollama"),
    )


def generate_chat(request: ChatRequest) -> ChatResponse:
    backend = os.getenv("LLM_BACKEND", "mock").lower()
    if backend == "mock":
        return _mock_chat(request)
    if backend in {"ollama", "openai-compatible"}:
        return _openai_compatible_chat(request)
    raise HTTPException(status_code=500, detail=f"Unsupported LLM_BACKEND: {backend}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "backend": os.getenv("LLM_BACKEND", "mock")}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return generate_chat(request)


@app.post("/compare", response_model=CompareResponse)
def compare(request: CompareRequest) -> CompareResponse:
    """Run the same model and messages at three temperatures."""
    results: list[CompareResult] = []
    for temperature in (0.0, 0.7, 1.5):
        chat_result = generate_chat(
            ChatRequest(
                model=request.model,
                messages=request.messages,
                temperature=temperature,
            )
        )
        results.append(
            CompareResult(
                temperature=temperature,
                response=chat_result.response,
                latency_ms=chat_result.latency_ms,
                usage=chat_result.usage,
            )
        )
    return CompareResponse(model=request.model, results=results)
