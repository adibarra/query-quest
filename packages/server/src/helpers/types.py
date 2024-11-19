# @author: adibarra (Alec Ibarra)
# @description: Types for the server

from datetime import datetime
from typing import Optional, TypedDict


class QuestionWithTagsDict(TypedDict):
    id: int
    question: str
    difficulty: int
    options: list[str]
    tags: list[int]


class QuestionDict(TypedDict):
    id: int
    question: str
    difficulty: int
    option1: str
    option2: str
    option3: Optional[str]
    option4: Optional[str]


class QuestionTagDict(TypedDict):
    question_id: int
    tag_id: int


class SessionDict(TypedDict):
    user_uuid: str
    token: str
    created_at: datetime


class StatisticsDict(TypedDict):
    user_uuid: str
    xp: int
    wins: int
    losses: int


class TagDict(TypedDict):
    id: int
    name: str
    description: str


class UserDict(TypedDict):
    uuid: str
    username: str
    password_hash: str
