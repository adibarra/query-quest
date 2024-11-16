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
        return QuestionResponse(code=404, message="No questions found", data=None)
    return QuestionResponse(code=200, message="Ok", data=questions)


@router.post(
    "/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED
)
def create_question(request: QuestionRequest):
    try:
        new_question_id = db.create_question(request)
        return QuestionResponse(
            code=201,
            message=f"Question created with id {new_question_id}",
            data=None,
        )
    except Exception as e:
        print(f"Error creating question: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Failed to create the question")


@router.delete(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def delete_question(question_id: int):
    try:
        if db.delete_question(question_id):
            return QuestionResponse(
                code=200, message="Question deleted successfully", data=None
            )
        return QuestionResponse(code=404, message="Question not found", data=None)
    except Exception as e:
        print(f"Error deleting question: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Failed to delete the question")
