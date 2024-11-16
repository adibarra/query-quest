# @author: Adi-K527
# @description: Questions routes for the API

from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class QuestionData(BaseModel):
    id: int
    question: str
    difficulty: int
    option1: str
    option2: str
    option3: Optional[str] = None
    option4: Optional[str] = None


class QuestionRequest(BaseModel):
    question: str
    difficulty: int
    option1: str
    option2: str
    option3: Optional[str] = None
    option4: Optional[str] = None


class QuestionResponse(BaseModel):
    code: int
    message: str
    data: Optional[list[QuestionData]] = None


@router.get(
    "/questions", response_model=QuestionResponse, status_code=status.HTTP_200_OK
)
def get_questions():
    questions = db.get_all_questions()
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return QuestionResponse(code=200, message="Ok", data=questions)


@router.get(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def get_question(question_id: int):
    question = db.get_one_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return QuestionResponse(code=200, message="Ok", data=question)


@router.post(
    "/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED
)
def create_question(request: QuestionRequest):
    new_question_data = db.create_question(request)
    if not new_question_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return QuestionResponse(code=200, message="Ok", data=new_question_data)


@router.delete(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def delete_question(question_id: int):
    if not db.delete_question(question_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    return QuestionResponse(code=200, message="Ok")
