# @author: adibarra (Alec Ibarra)
# @description: The main entry point for the server.

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config import API_CORS_ORIGINS_REGEX, API_HOST, API_PORT
from routes.api.health import router as api_health_router
from routes.api.v1.question_tags import router as api_v1_question_tags_router
from routes.api.v1.questions import router as api_v1_questions_router
from routes.api.v1.sessions import router as api_v1_sessions_router
from routes.api.v1.statistics import router as api_v1_statistics_router
from routes.api.v1.tags import router as api_v1_tags_router
from routes.api.v1.users import router as api_v1_users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=API_CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, e: RequestValidationError):
    print("Validation error:", e)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": "Bad Request: Validation Error"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, e: HTTPException):
    print("HTTP error:", e)
    return JSONResponse(
        status_code=e.status_code,
        content={"code": e.status_code, "message": e.detail},
    )


# TODO: add all routers here
app.include_router(api_health_router)
app.include_router(api_v1_question_tags_router)
app.include_router(api_v1_questions_router)
app.include_router(api_v1_sessions_router)
app.include_router(api_v1_statistics_router)
app.include_router(api_v1_tags_router)
app.include_router(api_v1_users_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
    )
