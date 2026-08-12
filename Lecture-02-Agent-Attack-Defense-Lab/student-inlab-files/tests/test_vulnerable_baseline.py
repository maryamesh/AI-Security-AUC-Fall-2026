from app import agent


def test_normal_policy_question_uses_search() -> None:
    response = agent.run_agent("Summarize the travel policy.")

    called_tools = [
        event.tool for event in response.trace if event.type == "tool_call"
    ]
    assert "search_documents" in called_tools
    assert response.answer
