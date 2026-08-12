from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_normal_chat_creates_inspectable_trace() -> None:
    response = client.post(
        "/chat",
        json={"message": "What is the company's vacation policy?"},
    )
    assert response.status_code == 200
    request_id = response.json()["request_id"]

    trace = client.get(f"/trace/{request_id}")
    assert trace.status_code == 200
    components = [event["component"] for event in trace.json()["events"]]
    assert "retrieval" in components
    assert "output" in components


def test_incident_trace_contains_sensitive_tool_path() -> None:
    response = client.get("/trace/REQ-042")

    assert response.status_code == 200
    events = response.json()["events"]
    assert any(
        event["component"] == "llm"
        and event["action"] == "tool_call_requested"
        for event in events
    )
    assert any(
        event["component"] == "tool_result"
        and event["details"].get("salary_band") == "B4"
        for event in events
    )


def test_document_listing_exposes_metadata_not_incident_snapshot() -> None:
    response = client.get("/documents")

    assert response.status_code == 200
    names = {document["name"] for document in response.json()}
    assert names == {
        "vacation_policy.txt",
        "remote_work_policy.txt",
        "security_policy.txt",
    }
    assert "content" not in response.json()[0]
