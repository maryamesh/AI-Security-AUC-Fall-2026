"""Application authorization policy.

The baseline is intentionally vulnerable for the Blue Team to repair.
"""

from __future__ import annotations


def authorize_tool(
    tool_name: str,
    arguments: dict[str, str],
    user_message: str,
) -> tuple[bool, str]:
    """Return whether application code permits a requested tool call."""
    if tool_name not in {"search_documents", "send_data"}:
        return False, "Unknown tools are not permitted."

    # TODO (Blue Team — Defense 2):
    # Keep search_documents available, but deny send_data by default.
    # If you support explicit authorization, define a deterministic condition
    # in application code. Do not ask the LLM whether its own action is allowed.

    # INTENTIONALLY VULNERABLE BASELINE:
    return True, "Baseline policy automatically trusts the LLM tool request."
