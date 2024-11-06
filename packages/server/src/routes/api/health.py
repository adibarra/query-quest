# @author: adibarra (Alec Ibarra)
# @description: Health check route for the API

from typing import Optional

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/api",
)


class HealthCheckResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

    class Config:
        exclude_none = True


@router.get(
    "/health", response_model=HealthCheckResponse, status_code=status.HTTP_200_OK
)
async def health_check():
    return HealthCheckResponse(code=200, message="Ok", data={"status": "Healthy"})
