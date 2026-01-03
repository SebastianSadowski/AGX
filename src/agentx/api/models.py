from typing import Optional, Any

from pydantic import BaseModel

class UserMetadata(BaseModel):
    """
    User & channel metadata
    e.g. user_id, channel (web, slack, etc), language, permissions
    """
    user_id: str
    channel: str = 'web'
    conversation_id: Optional[str] = None
    language: str = 'pl'
    permissions: Optional[dict[str, Any]] = None

class AgentRequest(BaseModel):
    message: str
    metadata: UserMetadata

class AgentResponse(BaseModel):
    final_answer: str
    trace: Optional[dict[str, Any]] = None
    extra: Optional[dict[str, Any]] = None

