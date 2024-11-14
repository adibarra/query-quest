# @author: adibarra (Alec Ibarra)
# @description: The main entry point for the server.

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config import API_CORS_ORIGINS, API_HOST, API_PORT
from routes.api.health import router as api_health_router
from routes.api.v1.sessions import router as api_v1_sessions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def not_found_exception_handler(request, e):
    print("Not found error:", e)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": 404, "message": 'Not Found'},
    )


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, e):
    print("Validation error:", e)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": "Bad Request"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, e):
    print("HTTP error:", e)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": 500, "message": "Internal Server Error"},
    )


# TODO: add all routers here
app.include_router(api_health_router)
app.include_router(api_v1_sessions_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
    )
