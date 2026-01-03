"""
ContextBuilder - builds context for agent based on request.

Final version should contains details such:
-conversation history
-longterm memory
-user details
"""

from agentx.api.models import AgentRequest
from agentx.core.types import Context


class ContextBuilder:

    def build(self, request: AgentRequest) -> Context:
        metadata = request.metadata

        context: Context= {
            "user_id": metadata.user_id,
            "channel": metadata.channel,
            "conversation_id": metadata.conversation_id,
            "language": metadata.language
        }

        return context

