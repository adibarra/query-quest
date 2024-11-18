# @author: adibarra (Alec Ibarra)
# @description: Sessions routes for the API

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import UUID4, BaseModel

from helpers.auth import Auth
from helpers.requireAuth import requireAuth
from helpers.types import SessionDict
from services.database import Database

db = Database()
router = APIRouter(
    prefix="/api/v1",
)


class SessionData(BaseModel):
    user_uuid: UUID4
    token: UUID4
    created_at: datetime


class SessionRequest(BaseModel):
    username: str
    password: str


class SessionResponse(BaseModel):
    code: int
    message: str
    data: Optional[SessionData] = None

    class Config:
        exclude_none = True


@router.post(
    "/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED
)
def create_session(
    data: SessionRequest = Body(...),
):
    user = db.get_user(username=data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found: User not found",
        )

    if not Auth.verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Incorrect password",
        )

    session = db.create_session(str(user["uuid"]))
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Could not create session",
        )

    return SessionResponse(code=201, message="Created", data=session)


@router.delete(
    "/sessions", response_model=SessionResponse, status_code=status.HTTP_200_OK
)
def delete_session(
    session: SessionDict = Depends(requireAuth),
):
    if not db.delete_session(token=session["token"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found: Session not found",
        )

    return SessionResponse(code=200, message="Ok")
