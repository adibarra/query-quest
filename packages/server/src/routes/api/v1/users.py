# @author: chipterpill
# @description: The user routes for the API.

from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4, BaseModel

from helpers.auth import Auth
from helpers.requireAuth import requireAuth
from helpers.types import SessionDict
from services.database import Database

db = Database()
router = APIRouter(prefix="/api/v1")


class CreateUserRequest(BaseModel):
    username: str
    password: str


class UserData(BaseModel):
    uuid: UUID4
    username: str

    class Config:
        extra = "ignore"


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    code: int
    message: str
    data: Optional[UserData] = None

    class Config:
        exclude_none = True


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(data: CreateUserRequest = Body(...)):
    try:
        Auth.validate_username(data.username)
        Auth.validate_password(data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request: Username or password invalid",
        )

    user = db.create_user(data.username, Auth.hash_password(data.password))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict: User already exists",
        )

    return UserResponse(code=201, message="Created", data=user)


@router.get(
    "/users/{uuid}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    uuid: UUID4 = Path(...),
    session: SessionDict = Depends(requireAuth),
):
    if str(uuid) != session["user_uuid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: User does not have permission",
        )

    user = db.get_user(uuid=str(uuid))
    user["password_hash"] = None
    return UserResponse(code=200, message="Ok", data=user)


@router.patch(
    "/users/{uuid}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def patch_user(
    uuid: UUID4 = Path(...),
    data: UpdateUserRequest = Body(...),
    session: SessionDict = Depends(requireAuth),
):
    if str(uuid) != session["user_uuid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: User does not have permission",
        )

    try:
        if data.username is not None:
            Auth.validate_username(data.username)
        if data.password is not None:
            Auth.validate_password(data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request: Username or password invalid",
        )

    # TODO: db.update_user does not exist
    if not db.update_user(
        str(uuid),
        data.username,
        Auth.hash_password(data.password) if data.password else None,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict",
        )

    user = db.get_user(uuid=str(uuid))
    user["password_hash"] = None
    return UserResponse(code=200, message="Ok", data=user)


@router.delete(
    "/users/{uuid}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def delete_user(
    uuid: UUID4 = Path(...),
    session: SessionDict = Depends(requireAuth),
):
    if str(uuid) != session["user_uuid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: User does not have permission",
        )

    if not db.delete_user(uuid=str(uuid)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return UserResponse(code=200, message="Ok")
