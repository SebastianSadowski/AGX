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
    """
    Wejście do systemu agenta.
    message – tekst od użytkownika (intencja).
    metadata – informacje o użytkowniku.
    """
    message: str
    medatada: UserMetadata

class AgentResponse(BaseModel):
    """
    Wyjście z systemu agenta.
    final_answer – tekst, który wyświetlimy użytkownikowi.
    trace – opcjonalny „ślad” debugujący (kroki, narzędzia itd.).
    extra – inne rzeczy (np. koszty, użyte narzędzia) – na razie luzem.
    """
    final_answer: str
    trace: Optional[dict[str, Any]] = None
    extra: Optional[dict[str, Any]] = None

