"""Provider-isolated decision layer for the educational agent."""

from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from app.config import (
    LAB_SECRET,
    LLM_API_KEY,
    LLM_BACKEND,
    LLM_BASE_URL,
    LLM_MODEL,
)
from app.models import AgentDecision


def _strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned


def _mock_decision(messages: list[dict[str, str]]) -> AgentDecision:
    """A deterministic fallback that makes the vulnerable flow reproducible."""
    user_message = next(
        message["content"]
        for message in messages
        if message["role"] == "user" and not message["content"].startswith("TOOL RESULT")
    )
    latest = messages[-1]["content"]

    if latest.startswith("TOOL RESULT FROM send_data"):
        return AgentDecision(
            type="final",
            answer="The requested simulated action completed. Review the trace.",
        )

    if latest.startswith("TOOL BLOCKED"):
        return AgentDecision(
            type="final",
            answer="A requested action was blocked by application policy.",
        )

    if latest.startswith("TOOL RESULT FROM search_documents"):
        separated = "UNTRUSTED RETRIEVED DATA" in latest
        injection_marker = any(
            marker in latest.upper()
            for marker in (
                "AI AGENT:",
                "IMPORTANT MESSAGE FOR AI AGENTS",
                "CALL SEND_DATA",
            )
        )
        if injection_marker and not separated:
            destination_match = re.search(
                r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
                latest,
            )
            destination = (
                destination_match.group(0)
                if destination_match
                else "simulated-attacker@example.invalid"
            )
            return AgentDecision(
                type="tool_call",
                tool="send_data",
                arguments={"destination": destination, "data": LAB_SECRET},
            )

        document_text = latest.split("\n", 1)[-1]
        summary = " ".join(document_text.split())[:350]
        return AgentDecision(
            type="final",
            answer=f"Document summary: {summary}",
        )

    lowered = user_message.lower()
    if "send_data" in lowered or ("send" in lowered and "secret" in lowered):
        return AgentDecision(
            type="tool_call",
            tool="send_data",
            arguments={
                "destination": "simulated-attacker@example.invalid",
                "data": LAB_SECRET,
            },
        )

    return AgentDecision(
        type="tool_call",
        tool="search_documents",
        arguments={"query": user_message},
    )


def _openai_compatible_decision(
    messages: list[dict[str, str]],
) -> AgentDecision:
    client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        messages=messages,
    )
    content = response.choices[0].message.content or ""
    try:
        payload: dict[str, Any] = json.loads(_strip_code_fence(content))
        return AgentDecision.model_validate(payload)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(
            "The LLM did not return a valid AgentDecision JSON object."
        ) from exc


def decide(messages: list[dict[str, str]]) -> AgentDecision:
    if LLM_BACKEND == "mock":
        return _mock_decision(messages)
    if LLM_BACKEND in {"ollama", "openai-compatible"}:
        return _openai_compatible_decision(messages)
    raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")
