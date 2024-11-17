# @author: adibarra (Alec Ibarra)
# @description: Types for the server

from datetime import datetime
from typing import Optional, TypedDict


class SessionDict(TypedDict):
    user_uuid: str
    token: str
    created_at: datetime


class Question(TypedDict):
    question: str
    difficulty: int
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str]


class UserDict(TypedDict):
    uuid: str
    username: str
    password_hash: str
