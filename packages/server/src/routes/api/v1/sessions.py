# @author: adibarra (Alec Ibarra)
# @description: Sessions routes for the API

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
    owner: UUID4
    token: UUID4


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
    "/sessions", response_model=SessionResponse, status_code=status.HTTP_200_OK
)
def create_session(
    data: SessionRequest = Body(...),
):
    # Check if user exists
    user = db.get_user_by_username(data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    # Verify password
    if not Auth.verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # User has been authenticated, create a session
    session = db.create_session(str(user["uuid"]))
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return SessionResponse(code=200, message="Ok", data=session)


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
