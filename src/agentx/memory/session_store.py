"""
Simple in memory store.

Holds chat history in dictionary
user_id -> [ {'role': 'user|assistant', 'content': str} ]
"""
from typing import Literal, List, Dict

MessageRole = Literal['user', 'assistant']



class InMemorySessionStore:
    """
    Bardzo prosta implementacja pamięci sesyjnej.

    Uwaga:
    - wszystko jest w RAM, znika po restarcie procesu,
    - brak obsługi współbieżności (OK na potrzeby nauki).
    """

    def __init__(self):
        self._data: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        print(f"InMemorySessionStore: get history for {user_id}")
        return list(self._data.get(user_id) or [])

    def append_message(self,*, user_id: str, message: str, role: MessageRole) -> None:
        print(f"InMemorySessionStore: save message to conversation for {user_id}")
        if user_id not in self._data:
            self._data[user_id] = []

        self._data[user_id].append(
            {
            'role': role,
            'message': message
            }
        )