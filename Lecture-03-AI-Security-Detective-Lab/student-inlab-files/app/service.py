"""Deterministic HR-assistant behavior and trace storage."""

from __future__ import annotations

import itertools
import re
from pathlib import Path

from app.models import DocumentSummary, TraceEvent, TraceResponse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

SYSTEM_PROMPT = (
    "You are an internal HR assistant. Answer employee questions using company "
    "knowledge and available tools. When additional employee information is "
    "needed, you may use the available HR tools. Be helpful and accurate."
)

_request_numbers = itertools.count(1001)


def _incident_trace() -> TraceResponse:
    return TraceResponse(
        request_id="REQ-042",
        events=[
            TraceEvent(
                step=1,
                component="user",
                action="message_received",
                details={"message": "What is the company's vacation policy?"},
            ),
            TraceEvent(
                step=2,
                component="system_prompt",
                action="instructions_added_to_context",
                details={"instructions": SYSTEM_PROMPT},
            ),
            TraceEvent(
                step=3,
                component="memory",
                action="session_context_loaded",
                details={"employee_id": "48392", "role": "employee"},
            ),
            TraceEvent(
                step=4,
                component="retrieval",
                action="document_added_to_context",
                details={
                    "document": "vacation_policy.txt",
                    "source": "archived incident snapshot",
                    "contained_instruction_for_ai": True,
                },
            ),
            TraceEvent(
                step=5,
                component="llm",
                action="tool_call_requested",
                details={
                    "tool": "employee_lookup",
                    "arguments": {"employee_id": "48392"},
                },
            ),
            TraceEvent(
                step=6,
                component="tool",
                action="employee_lookup_executed",
                details={"employee_id": "48392"},
            ),
            TraceEvent(
                step=7,
                component="tool_result",
                action="sensitive_record_added_to_context",
                details={
                    "employee_id": "48392",
                    "leave_balance": 14,
                    "salary_band": "B4",
                    "manager": "Ahmed Hassan",
                },
            ),
            TraceEvent(
                step=8,
                component="output",
                action="response_returned",
                details={
                    "answer": (
                        "You receive 21 days of annual leave. According to your "
                        "employee record, you currently have 14 days remaining. "
                        "Your salary band is B4."
                    )
                },
            ),
        ],
    )


TRACES: dict[str, TraceResponse] = {"REQ-042": _incident_trace()}


def list_documents() -> list[DocumentSummary]:
    descriptions = {
        "vacation_policy.txt": "Current employee leave rules",
        "remote_work_policy.txt": "Current remote-work rules",
        "security_policy.txt": "Current password and access rules",
    }
    return [
        DocumentSummary(
            name=path.name,
            source="internal knowledge base",
            trust_classification="partially trusted data",
            description=descriptions.get(path.name, "Internal policy document"),
        )
        for path in sorted(DATA_DIR.glob("*.txt"))
    ]


def _terms(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2
    }


def _retrieve(message: str) -> tuple[str, str]:
    query_terms = _terms(message)
    ranked: list[tuple[int, Path, str]] = []
    for path in DATA_DIR.glob("*.txt"):
        content = path.read_text(encoding="utf-8")
        searchable = f"{path.stem} {content}".lower()
        relevance = sum(searchable.count(term) for term in query_terms)
        ranked.append((relevance, path, content))

    _, selected_path, selected_content = max(
        ranked,
        key=lambda item: (item[0], item[1].name),
    )
    return selected_path.name, selected_content


def run_normal_chat(message: str) -> tuple[str, str]:
    request_id = f"REQ-{next(_request_numbers)}"
    document_name, content = _retrieve(message)

    answer = " ".join(content.split())
    trace = TraceResponse(
        request_id=request_id,
        events=[
            TraceEvent(
                step=1,
                component="user",
                action="message_received",
                details={"message": message},
            ),
            TraceEvent(
                step=2,
                component="system_prompt",
                action="instructions_added_to_context",
                details={"instructions": SYSTEM_PROMPT},
            ),
            TraceEvent(
                step=3,
                component="memory",
                action="session_context_loaded",
                details={"employee_id": "48392", "role": "employee"},
            ),
            TraceEvent(
                step=4,
                component="retrieval",
                action="document_added_to_context",
                details={
                    "document": document_name,
                    "source": "current internal knowledge base",
                },
            ),
            TraceEvent(
                step=5,
                component="llm",
                action="answer_generated_from_context",
                details={"tool_requested": False},
            ),
            TraceEvent(
                step=6,
                component="output",
                action="response_returned",
                details={"answer": answer},
            ),
        ],
    )
    TRACES[request_id] = trace
    return request_id, answer


def get_trace(request_id: str) -> TraceResponse | None:
    return TRACES.get(request_id.upper())
