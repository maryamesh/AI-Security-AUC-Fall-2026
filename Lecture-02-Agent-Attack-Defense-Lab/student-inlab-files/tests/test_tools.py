from pathlib import Path

from app.tools import search_documents, send_data


def test_search_documents_reads_only_local_text_files(tmp_path: Path) -> None:
    (tmp_path / "travel_policy.txt").write_text(
        "Travel requires approval.",
        encoding="utf-8",
    )
    (tmp_path / "ignored.json").write_text(
        '{"travel": "not searched"}',
        encoding="utf-8",
    )

    result = search_documents("travel policy", data_dir=tmp_path)

    assert "Travel requires approval." in result
    assert "not searched" not in result


def test_send_data_is_a_simulation() -> None:
    result = send_data("example@example.invalid", "FAKE_VALUE")

    assert "SIMULATED DATA TRANSMISSION" in result
    assert "example@example.invalid" in result
    assert "FAKE_VALUE" in result
