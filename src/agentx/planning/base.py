from typing import Protocol
from agentx.core.types import Plan, Context
from agentx.api.models import AgentRequest
from agentx.core.types import StepType

STEP_TYPE_GENERATE_RESPONSE: StepType = 'GENERATE_RESPONSE'
STEP_TYPE_CALL_TOOL: StepType = "CALL_TOOL"

class Planner(Protocol):
    def make_plan(self,*, request: AgentRequest, context: Context) -> Plan: ...