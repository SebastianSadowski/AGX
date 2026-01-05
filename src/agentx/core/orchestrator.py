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

from agentx.memory.session_store import MessageRole


class Orchestrator:
    def __init__(self, context_builder: Optional[ContextBuilder] = None, session_store: Optional[InMemorySessionStore] = None ):
        print('hello')
        self.session_store= session_store or InMemorySessionStore()
        self.context_builder = context_builder or ContextBuilder(self.session_store)


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
        final_text = (
            f"[orchestrator] Kanał={channel}, user={user_id}, "
            f"wiadomości w historii: {history_len}. "
            f"Ostatnia wiadomość: {message}"
        )


        # here - composes trace log
        trace = {
            "steps": [
                "orchestrator_start",
                "single_step_reply",
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

    def _update_session(self, user_id: str, message: str, role=MessageRole) -> None:
        self.session_store.append_message(user_id=user_id, message=message, role=role)
