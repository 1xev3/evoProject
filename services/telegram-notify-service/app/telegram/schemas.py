from enum import Enum
from dataclasses import dataclass


class HTTP_METHODS(Enum):
    GET = "GET"
    POST = "POST"

@dataclass
class BasicReponse():
    ok: str
    result: dict

@dataclass
class User():
    id: int = None
    is_bot: bool = None
    first_name: str = None
    last_name: str = None
    username: str = None
    can_join_groups: bool = None
    can_read_all_group_messages: bool = None
    supports_inline_queries: bool = None

@dataclass
class Chat(User):
    type: str = None

@dataclass
class Message():
    message_id: int
    from_user: User
    chat: Chat
    date: int
    text: str