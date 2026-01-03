"""
dummy API class. Further implementation will

"""
from .models import AgentRequest, AgentResponse
from ..core.orchestrator import Orchestrator

_orchestrator = Orchestrator()

def handle_request(request: AgentRequest) -> AgentResponse:
    return _orchestrator.run(request)

