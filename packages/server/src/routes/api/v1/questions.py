# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Questions routes for the API

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from helpers.requireAuth import requireAuth
from helpers.types import SessionDict
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class QuestionData(BaseModel):
    id: int
    question: str
    difficulty: int
    options: List[str]
    tags: List[int]


class QuestionRequest(BaseModel):
    question: str
    difficulty: int
    options: List[str]
    tags: List[int]


class QuestionResponse(BaseModel):
    code: int
    message: str
    data: List[QuestionData] = None

    class Config:
        exclude_none = True


@router.get(
    "/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def get_questions(
    session: SessionDict = Depends(requireAuth),
):
    questions = db.get_questions()
    return QuestionResponse(code=200, message="Ok", data=questions)


@router.get(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def get_question(
    question_id: int,
    session: SessionDict = Depends(requireAuth),
):
    question = db.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found",
        )

    return QuestionResponse(code=200, message="Ok", data=[question])


# TODO: broken, needs to handle tags
# @router.post(
#     "/questions",
#     response_model=QuestionResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_question(
#     request: QuestionRequest,
#     session: SessionDict = Depends(requireAuth),
# ):
#     options = request.option_fields
#
#     new_question_id = db.create_question(
#         question=request.question,
#         difficulty=request.difficulty,
#         **options
#     )
#
#     if not new_question_id:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to create the question",
#         )
#
#     if request.tags:
#         db.add_tags_to_question(new_question_id, request.tags)
#
#     new_question_data = db.get_question(new_question_id)
#
#     return QuestionResponse(code=201, message="Created", data=[new_question_data])


# @router.delete(
#     "/questions/{question_id}",
#     response_model=QuestionResponse,
#     status_code=status.HTTP_200_OK,
# )
# def delete_question(
#     question_id: int,
#     session: SessionDict = Depends(requireAuth),
# ):
#     if not db.delete_question(question_id):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Question with id {question_id} not found",
#         )
#
#     return QuestionResponse(code=200, message="Ok")
