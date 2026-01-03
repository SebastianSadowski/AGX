"""
dummy API class. Further implementation will


"""

from models import AgentRequest, AgentResponse

def handle_request(request: AgentRequest) -> AgentResponse:
    user_id = request.medatada.user_id
    channel = request.medatada.channel
    message = request.message

    final_text = f"[stub] Użytkownik {user_id} napisał: {message}, na kanale {channel}"

    return AgentResponse(
        final_answer=final_text,
        trace={"steps": ["gateway_stub"]},
        extra={"version": "0.0.1"})
