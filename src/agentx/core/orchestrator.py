"""
Orchestrator - decomposes goal to steps, decides which agent/tool should be involved to the specific task.
flow:
- get request
- build context
- generate simple answer
- return AgentResponse


Input: request (AgentRequest)
Output: AgentResponse

"""
from agentx.api.models import AgentResponse
from agentx.core.types import PlanStep
from agentx.memory.context_builder import *
from typing import Optional

from agentx.memory.session_store import MessageRole
from agentx.planning.base import Planner, STEP_TYPE_GENERATE_RESPONSE, STEP_TYPE_CALL_TOOL
from agentx.planning.simple_planner import SimplePlanner


class Orchestrator:
    def __init__(self, context_builder: Optional[ContextBuilder] = None, session_store: Optional[InMemorySessionStore] = None, planner: Optional[Planner] = None):
        self.session_store= session_store or InMemorySessionStore()
        self.context_builder = context_builder or ContextBuilder(self.session_store)
        self.planner: Planner = planner or SimplePlanner()


    def run(self, request: AgentRequest) -> AgentResponse:
        """
        dummy implementation - initial scope, create interface between API & orchestrator.

        :param request: AgentRequest
        :return: AgentResponse
        """

        #here - fetch context & append user message
        context: Context = self.context_builder.build(request)

        user_id = request.metadata.user_id
        channel = request.metadata.channel
        message = request.message
        history = context.get('history', [])

        self._update_session(user_id, message, 'user')
        # here - composes response message
        history_len = len(history)

        plan = self.planner.make_plan(request=request, context=context)

        plan_response = self._handle_step(plan.steps[0])


        final_text = (
            f"[orchestrator] Kanał={channel}, user={user_id}, "
            f"wiadomości w historii: {history_len}. "
            f"Ostatnia wiadomość: {message}"
            f"\n odpowiedz z planu {plan_response}"
        )


        # here - composes trace log
        trace = {
            "plan": {
                "steps_amount": len(plan.steps),
                "steps": [ st.description for st in plan.steps]

            },
            "steps": [
                "orchestrator_start",
                "single_step_reply",
                *[f"{st.description} ({st.step_type})" for st in plan.steps],
                "orchestrator_end"
            ],
            "context_summary":{
                "history_length": history_len,
                "language": context.get("language"),
            }
        }

        # here - composes extra dictionary

        extra = {
            "version": "0.0.3",
            "notes": "Orchestrator z contextem i historia konwersacji (brak planera, narzędzi itd.)",
        }


        response = AgentResponse(
            final_answer=final_text,
            trace=trace,
            extra=extra,
        )

        self._update_session(user_id, response.final_answer, 'assistant')
        return response

    def _update_session(self, user_id: str, message: str, role: MessageRole) -> None:
        self.session_store.append_message(user_id=user_id, message=message, role=role)

    def _handle_step(self, step: PlanStep):
        step_response: str = ""
        if step.step_type == STEP_TYPE_GENERATE_RESPONSE:
            print("Orchestrator._handle_step: step type GENERATE_RESPONSE…")
            step_response = "Typ kroku GENERATE_RESPONSE…"
        elif step.step_type== STEP_TYPE_CALL_TOOL:
            print("Orchestrator._handle_step: step type CALL_TOOL…")
            step_response = "Typ kroku CALL_TOOL"
        else:
            print("Orchestrator._handle_step: step type NOT_RECOGNIZED…")
            step_response = "Nie rozpoznano typu kroku, zwracam blad"

        return step_response