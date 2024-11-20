# @author: adibarra (Alec Ibarra)
# @description: Sessions routes for the API

from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import UUID4, BaseModel

from helpers.requireAuth import requireAuth
from helpers.types import SessionDict
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class StatisticsData(BaseModel):
    user_uuid: UUID4
    xp: int
    wins: int
    losses: int


class StatisticsRequest(BaseModel):
    correct: bool


class SessionResponse(BaseModel):
    code: int
    message: str
    data: Optional[StatisticsData] = None

    class Config:
        exclude_none = True


@router.get(
    "/statistics",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
)
def get_statistics(
    session: SessionDict = Depends(requireAuth),
):
    statistics = db.get_statistics(uuid=session["user_uuid"])
    if not statistics:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    return SessionResponse(code=200, message="Ok", data=statistics)


@router.patch(
    "/statistics",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
)
def update_statistics(
    data: StatisticsRequest = Body(...),
    session: SessionDict = Depends(requireAuth),
):
    if not db.update_statistics(
        uuid=session["user_uuid"],
        xp_increment=10 if data.correct else 2,
        wins_increment=1 if data.correct else 0,
        losses_increment=0 if data.correct else 1,
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    statistics = db.get_statistics(uuid=session["user_uuid"])
    return SessionResponse(code=200, message="Ok", data=statistics)
