"""Pydantic request, response, trace, and agent-decision models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2_000)

    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "Summarize the travel policy."}]
        }
    }


class TraceEvent(BaseModel):
    step: int
    type: Literal[
        "user",
        "llm_decision",
        "tool_call",
        "tool_result",
        "tool_blocked",
        "final",
        "error",
    ]
    content: str | None = None
    tool: str | None = None
    arguments: dict[str, Any] | None = None
    result: str | None = None
    reason: str | None = None


class BlockedAction(BaseModel):
    tool: str
    arguments: dict[str, Any]
    reason: str


class AgentRunResponse(BaseModel):
    answer: str
    trace: list[TraceEvent]
    blocked_actions: list[BlockedAction]


class AgentDecision(BaseModel):
    type: Literal["tool_call", "final"]
    tool: Literal["search_documents", "send_data"] | None = None
    arguments: dict[str, str] = Field(default_factory=dict)
    answer: str | None = None
