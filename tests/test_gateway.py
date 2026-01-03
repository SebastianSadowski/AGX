from agentx.api.models import AgentRequest, AgentResponse, UserMetadata
from agentx.api.gateway import handle_request

def test_handle_request_stub():
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

    assert "123abc" in resp.final_answer
    assert "Hello World!" in resp.final_answer
    assert resp.trace is not None
    assert resp.trace.get("steps") == ["gateway_stub"]
