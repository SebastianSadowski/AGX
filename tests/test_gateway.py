from agentx.api.models import AgentRequest, AgentResponse, UserMetadata
from agentx.api.gateway import handle_request

def test_handle_single_request():
    metadata = UserMetadata(
        user_id="123abc",
        conversation_id="123-abc-123",
        permissions=None
    )
    req = AgentRequest(
        metadata=metadata,
        message="Hello World!"
    )

    resp = handle_request(req)
    print(resp.final_answer)
    print(resp.trace)


    #assert general
    assert "123abc" in resp.final_answer
    assert "Hello World!" in resp.final_answer

    #assert trace
    assert resp.trace is not None
    steps = resp.trace.get("steps", [])
    context_summary = resp.trace.get("context_summary", {})

    assert "orchestrator_start" in steps
    assert "single_step_reply" in steps
    assert "orchestrator_end" in steps

    history_length = context_summary.get('history_length')
    assert "history_length" in context_summary
    assert isinstance(history_length, int)
    assert history_length is 0

    #assert extra
    assert resp.extra is not None
    assert resp.extra.get("version") == "0.0.3"


def test_handle_conversation_request():
    metadata = UserMetadata(
        user_id="123abc",
        conversation_id="123-abc-123",
        permissions=None
    )
    message1 = AgentRequest(
        metadata=metadata,
        message="Hello World!"
    )
    message2 = AgentRequest(
        metadata=metadata,
        message="Message 2"
    )


    resp1 = handle_request(message1)
    print(resp1.final_answer)
    print(resp1.trace)
    resp = handle_request(message1)
    print(resp.final_answer)
    print(resp.trace)


    #assert general
    assert "123abc" in resp.final_answer
    assert "Hello World!" in resp.final_answer

    #assert trace
    assert resp.trace is not None
    steps = resp.trace.get("steps", [])
    context_summary = resp.trace.get("context_summary", {})

    assert "orchestrator_start" in steps
    assert "single_step_reply" in steps
    assert "orchestrator_end" in steps

    history_length = context_summary.get('history_length')
    assert "history_length" in context_summary
    assert isinstance(history_length, int)
    assert history_length is 2

    #assert extra
    assert resp.extra is not None
    assert resp.extra.get("version") == "0.0.3"
