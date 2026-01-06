from typing import Any, Dict, Literal, List, Optional
from pydantic import BaseModel

Context = Dict[str, Any]
StepType = Literal["GENERATE_RESPONSE", "CALL_TOOL"]


class PlanStep(BaseModel):
    step_type: StepType
    description: str #short explanation e.g. explain to user, call math tool
    tool_name: Optional[str] = None
    params: Optional[dict] = None

class Plan(BaseModel):
    steps: List[PlanStep]


