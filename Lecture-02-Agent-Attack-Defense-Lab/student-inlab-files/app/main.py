"""FastAPI entry point for the controlled agent-security lab."""

from __future__ import annotations

from fastapi import FastAPI

from app.agent import run_agent
from app.config import LLM_BACKEND, LLM_MODEL
from app.models import AgentRunRequest, AgentRunResponse

app = FastAPI(
    title="Lab 2 — Attack and Defend an LLM Agent",
    description=(
        "A local educational simulation with an explicit agent loop, local "
        "document search, and a non-networked data-transmission tool."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "llm_backend": LLM_BACKEND,
        "llm_model": LLM_MODEL,
    }


@app.post("/agent/run", response_model=AgentRunResponse)
def agent_run(request: AgentRunRequest) -> AgentRunResponse:
    return run_agent(request.message)
