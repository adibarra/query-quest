# @author: Adi-K527 (Adi Kandakurtikar)
# @description: Tags routes for the API

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


class TagData(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        exclude_none = True


class TagRequest(BaseModel):
    name: str
    description: str


class AssignTagsRequest(BaseModel):
    question_id: int
    tag_ids: List[int]


class TagResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[TagData]] = None

    class Config:
        exclude_none = True


@router.get(
    "/tags",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
def get_tags(
    session: SessionDict = Depends(requireAuth),
):
    tags = db.get_tags()
    return TagResponse(code=200, message="Ok", data=tags)


@router.get(
    "/tags/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag(
    tag_id: int,
    session: SessionDict = Depends(requireAuth),
):
    tag = db.get_tag(tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found",
        )

    return TagResponse(code=200, message="Ok", data=[tag])


@router.post(
    "/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    request: TagRequest,
    session: SessionDict = Depends(requireAuth),
):
    new_tag_data = db.create_tag(request)
    print(new_tag_data)
    if not new_tag_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the tag",
        )

    return TagResponse(code=201, message="Created", data=[new_tag_data])


@router.post(
    "/assign-tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_tags(
    request: AssignTagsRequest,
    session: SessionDict = Depends(requireAuth),
):
    new_tag_data = db.assign_tags(request)
    if not new_tag_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the tag",
        )

    return TagResponse(code=201, message="Tags assigned", data=[new_tag_data])


@router.delete(
    "/tags/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
def delete_tag(
    tag_id: int,
    session: SessionDict = Depends(requireAuth),
):
    if not db.delete_tag(tag_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found",
        )

    return TagResponse(code=200, message="Ok")
