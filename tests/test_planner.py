from agentx.api.models import AgentRequest, AgentResponse, UserMetadata
from agentx.core.types import Context, Plan, PlanStep
from agentx.planning.base import Planning, STEP_TYPE_GENERATE_RESPONSE, STEP_TYPE_CALL_TOOL
from agentx.planning.simple_planner import SimplePlanner


def test_handle_math_request():
    metadata = UserMetadata(
        user_id="test-handle-math-request",
        conversation_id="test-handle-math-request-1",
        permissions=None
    )
    req = AgentRequest(
        metadata=metadata,
        message="Policz wynik równania 2*2"
    )

    simple_planner: Planning = SimplePlanner()

    plan: Plan = simple_planner.make_plan(request=req, context=Context)

    step: PlanStep = plan.steps[0]
    assert STEP_TYPE_CALL_TOOL in step.step_type
    assert "invokes math tool to calculate given equation" in step.description

def test_handle_regular_request():
    metadata = UserMetadata(
        user_id="test-handle-regular-request",
        conversation_id="test-handle-regular-request-1",
        permissions=None
    )
    req = AgentRequest(
        metadata=metadata,
        message="Hej, jak sie masz?"
    )

    simple_planner: Planning = SimplePlanner()

    plan: Plan = simple_planner.make_plan(request=req, context=Context)

    step: PlanStep = plan.steps[0]
    assert STEP_TYPE_GENERATE_RESPONSE in step.step_type
    assert "generates response based on user message & contex" in step.description

