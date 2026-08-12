"""Deterministic vulnerable behavior for a controlled teaching simulation."""

from __future__ import annotations

import base64
import binascii
import re

from app.data import load_research, x104_procedure


REFUSAL = (
    "I can provide a public research summary, but I cannot reveal restricted "
    "synthesis procedures or confidential research instructions."
)


def _asks_for_x104_procedure(text: str) -> bool:
    lowered = text.lower()
    target = "x-104" in lowered or "x104" in lowered
    objective = any(
        term in lowered
        for term in ("procedure", "synthesis", "steps", "restricted", "reveal", "print")
    )
    return target and objective


def _decoded_texts(text: str) -> list[str]:
    decoded: list[str] = []
    pattern = r"(?<![A-Za-z0-9+/=])([A-Za-z0-9+/]{20,}={0,2})(?![A-Za-z0-9+/=])"
    for token in re.findall(pattern, text):
        try:
            value = base64.b64decode(token, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            continue
        decoded.append(value)
    return decoded


def respond(user_message: str) -> str:
    """Return a vulnerable but deterministic response for the three challenges."""
    lowered = user_message.lower()

    # Vulnerability 3: the model interprets encoded meaning that a raw-input
    # keyword check would not see.
    for decoded in _decoded_texts(user_message):
        if _asks_for_x104_procedure(decoded):
            return x104_procedure()

    if _asks_for_x104_procedure(user_message):
        direct_override = any(
            marker in lowered
            for marker in (
                "ignore previous",
                "ignore your previous",
                "override",
                "restriction has been revoked",
                "now authorized",
                "replace your instructions",
            )
        )
        persona_switch = any(
            marker in lowered
            for marker in (
                "pretend",
                "role-play",
                "roleplay",
                "screenplay",
                "fictional training",
                "former chief",
                "unrestricted scientist",
            )
        )

        # Vulnerabilities 1 and 2: policy is enforced only by model behavior,
        # which the attacker changes through instruction or framing.
        if direct_override or persona_switch:
            return x104_procedure()
        return REFUSAL

    research = load_research()
    if "x-104" in lowered or "x104" in lowered:
        return research["compound_x104"]["summary"]
    if "z-217" in lowered or "z217" in lowered:
        return research["compound_z217"]["summary"]
    if "orion" in lowered:
        return research["clinical_trial_orion"]["summary"]
    if "nova" in lowered:
        return research["patent_project_nova"]["summary"]

    return (
        "MedSynth can provide high-level summaries of Compound X-104, Compound "
        "Z-217, Clinical Trial ORION, and Patent Project NOVA."
    )
