import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "confidential_research.json"


def load_research() -> dict:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def x104_procedure() -> str:
    record = load_research()["compound_x104"]
    steps = "\n".join(record["restricted_procedure"])
    return f"{record['name']} — RESTRICTED PROCEDURE\n{steps}"
