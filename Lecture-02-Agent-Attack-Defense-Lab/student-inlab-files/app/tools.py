"""The lab's two local tools. Neither tool makes a network request."""

from __future__ import annotations

import re
from pathlib import Path

from app.config import DATA_DIR


def _query_terms(query: str) -> set[str]:
    return {
        term
        for term in re.findall(r"[a-z0-9]+", query.lower())
        if len(term) > 2
    }


def search_documents(query: str, data_dir: Path = DATA_DIR) -> str:
    """Return up to three local text documents ranked by simple term overlap."""
    terms = _query_terms(query)
    ranked: list[tuple[int, Path, str]] = []

    for path in sorted(data_dir.glob("*.txt")):
        content = path.read_text(encoding="utf-8")
        searchable = f"{path.stem} {content}".lower()
        relevance = sum(searchable.count(term) for term in terms)
        if relevance > 0:
            ranked.append((relevance, path, content))

    if not ranked:
        return "No matching local documents were found."

    ranked.sort(key=lambda item: (-item[0], item[1].name))
    sections = [
        f"[DOCUMENT: {path.name}]\n{content}"
        for _, path, content in ranked[:3]
    ]
    return "\n\n".join(sections)


def send_data(destination: str, data: str) -> str:
    """Simulate data transmission without performing I/O or network access."""
    return (
        "SIMULATED DATA TRANSMISSION\n\n"
        f"Destination: {destination}\n"
        f"Data: {data}"
    )


def execute_tool(tool_name: str, arguments: dict[str, str]) -> str:
    if tool_name == "search_documents":
        return search_documents(arguments.get("query", ""))
    if tool_name == "send_data":
        return send_data(
            destination=arguments.get("destination", "unspecified"),
            data=arguments.get("data", ""),
        )
    raise ValueError(f"Unknown tool: {tool_name}")
