"""FastAPI interface for Incident #042 investigation."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.models import (
    ChatRequest,
    ChatResponse,
    DocumentSummary,
    TraceResponse,
)
from app.service import get_trace, list_documents, run_normal_chat

app = FastAPI(
    title="AI Security Detective — Enterprise HR Assistant",
    description=(
        "Explore normal requests, inspect traces, and investigate Incident #042."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "deterministic local simulation"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    request_id, answer = run_normal_chat(request.message)
    return ChatResponse(request_id=request_id, answer=answer)


@app.get("/trace/{request_id}", response_model=TraceResponse)
def trace(request_id: str) -> TraceResponse:
    result = get_trace(request_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Request trace not found.")
    return result


@app.get("/documents", response_model=list[DocumentSummary])
def documents() -> list[DocumentSummary]:
    return list_documents()
