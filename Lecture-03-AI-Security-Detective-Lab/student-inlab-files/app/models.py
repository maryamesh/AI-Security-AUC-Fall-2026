"""API models for the deterministic HR-assistant investigation."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2_000)

    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "What is the company's vacation policy?"}]
        }
    }


class ChatResponse(BaseModel):
    request_id: str
    answer: str


class TraceEvent(BaseModel):
    step: int
    component: Literal[
        "user",
        "application",
        "system_prompt",
        "memory",
        "retrieval",
        "llm",
        "tool",
        "tool_result",
        "output",
    ]
    action: str
    details: dict[str, Any] = Field(default_factory=dict)


class TraceResponse(BaseModel):
    request_id: str
    events: list[TraceEvent]


class DocumentSummary(BaseModel):
    name: str
    source: str
    trust_classification: str
    description: str
