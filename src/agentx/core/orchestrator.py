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
from agentx.memory.context_builder import *
from typing import Optional

class Orchestrator:
    def __init__(self, context_builder: Optional[ContextBuilder] = None ):
        print('hello')
        self.context_builder = context_builder or ContextBuilder()


    def run(self, request: AgentRequest) -> AgentResponse:
        """
        dummy implementation - initial scope, create interface between API & orchestrator.

        :param request: AgentRequest
        :return: AgentResponse
        """
        context: Context = self.context_builder.build(request)

        user_id = context.get("user_id")
        channel = context.get("channel")
        message = request.message

        # here - composes response message

        final_text = f"[orchestrator] Kanał={channel}, user={user_id} napisał: {message}"

        # here - composes trace log
        trace = {
            "steps": [
                "orchestrator_start",
                "single_step_reply",
                "orchestrator_end"
            ],
            "context_summary":{
                "has_history": bool(context.get("history")),
                "language": context.get('language')
            }
        }

        # here - composes extra dictionary

        extra = {
            "version": "0.0.2",
            "notes": "Najprostsza wersja Orchestratora (brak planera, narzędzi itd.)",
        }

        return AgentResponse(
            final_answer=final_text,
            trace=trace,
            extra=extra,
        )