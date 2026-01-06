import re
from operator import contains
from typing import List

from agentx.api.models import AgentRequest
from agentx.core.types import Context, Plan, PlanStep
from agentx.planning.base import Planning, STEP_TYPE_CALL_TOOL, STEP_TYPE_GENERATE_RESPONSE


class SimplePlanner(Planning):
    def make_plan(self, request: AgentRequest, context: Context) -> Plan:
        steps: List[PlanStep] = []
        plan: Plan = Plan(steps=steps)

        message = request.message

        if re.search(r"[+\-*/]|\bpolicz\b|\bdodaj\b", message):
            print("SimplePlanner: contains math description - invokes math tool ---")
            steps.append(
                PlanStep(
                    step_type=STEP_TYPE_CALL_TOOL,
                    description="invokes math tool to calculate given equation",
                    tool_name="math",
                    params={"expression": message}
                )
            )
        else:
            print("SimplePlanner: ---no need to use tools, generating response ")
            steps.append(
                PlanStep(
                    step_type=STEP_TYPE_GENERATE_RESPONSE,
                    description="generates response based on user message & context"
                )
            )
        print('---- BELOW PLAN -----')
        plan: Plan = Plan(steps=steps)
        print(plan)
        return  plan

