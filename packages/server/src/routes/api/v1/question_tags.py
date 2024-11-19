# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Question tag routes for the API

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from helpers.requireAuth import requireAuth
from helpers.types import SessionDict
from pydantic import BaseModel
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class QuestionTagData(BaseModel):
    question_id: int
    tag_id: int

    class Config:
        exclude_none = True


class QuestionTagRequest(BaseModel):
    question_id: int
    tag_id: int


class QuestionTagResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[QuestionTagData]] = None

    class Config:
        exclude_none = True


@router.get(
    "/question-tags",
    response_model=QuestionTagResponse,
    status_code=status.HTTP_200_OK,
)
def get_tags(
    session: SessionDict = Depends(requireAuth),
):
    tags = db.get_question_tags()
    return QuestionTagResponse(code=200, message="Ok", data=tags)


@router.get(
    "/question-tags/{question_id}/{tag_id}",
    response_model=QuestionTagResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag(
    question_id: int,
    tag_id: int,
    session: SessionDict = Depends(requireAuth),
):
    question_tag = db.get_question_tag(question_id, tag_id)
    if not question_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question tag {(question_id, tag_id)} not found",
        )

    return QuestionTagResponse(code=200, message="Ok", data=[question_tag])


@router.post(
    "/create-question-tag",
    response_model=QuestionTagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question_tag(
    request: QuestionTagRequest,
    session: SessionDict = Depends(requireAuth),
):
    new_question_tag_data = db.create_question_tag(request)
    if not new_question_tag_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign tag to question",
        )

    return QuestionTagResponse(
        code=201, message="Created", data=[new_question_tag_data]
    )


@router.delete(
    "/question-tags/{question_id}/{tag_id}",
    response_model=QuestionTagResponse,
    status_code=status.HTTP_200_OK,
)
def delete_tag(
    question_id: int,
    tag_id: int,
    session: SessionDict = Depends(requireAuth),
):
    if not db.delete_question_tag(question_id, tag_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question tag {(question_id, tag_id)} not found",
        )

    return QuestionTagResponse(code=200, message="Ok")
