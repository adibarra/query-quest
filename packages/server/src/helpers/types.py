# @author: adibarra (Alec Ibarra)
# @description: Types for the server

from dataclasses import dataclass


@dataclass
class Question:
    """
    Dataclass representing a question.
    """

    question: str
    difficulty: int
    option1: str
    option2: str
    option3: str = None
    option4: str = None
