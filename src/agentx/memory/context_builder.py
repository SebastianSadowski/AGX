"""
ContextBuilder - builds context for agent based on request.

Final version should contains details such:
-conversation history
-longterm memory
-user details
"""

from agentx.api.models import AgentRequest
from agentx.core.types import Context
from agentx.memory.session_store import InMemorySessionStore



class ContextBuilder:
    def __init__(self, session_store: InMemorySessionStore):
        self._session_store = session_store

    def build(self, request: AgentRequest) -> Context:

        metadata = request.metadata
        user_id = request.metadata.user_id

        history = self._session_store.get_history(user_id)
        print(f'ContextBuilder: history: {history}')

        context: Context= {
            "user_id": user_id,
            "channel": metadata.channel,
            "conversation_id": metadata.conversation_id,
            "language": metadata.language,
            "history": history

        }

        return context

