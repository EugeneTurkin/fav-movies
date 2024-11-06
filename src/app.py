from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.auth.routes import router as auth_router
from src.movies.routes import router as movie_router
from src.shared.exceptions import (
    BadGatewayException,
    BadRequestException,
    InternalServerError,
    NotAllowedException,
    NotAuthenticatedException,
    NotFoundException,
)


if TYPE_CHECKING:
    from fastapi import Request


app = FastAPI()

app.include_router(auth_router)
app.include_router(movie_router)


@app.exception_handler(BadRequestException)
async def handle_bad_request(_: Request, exception: BadRequestException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "action": exception.action,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotAllowedException)
async def handle_not_allowed(_: Request, exception: NotAllowedException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "action": exception.action,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotAuthenticatedException)
async def handle_not_authenticated(_: Request, exception: NotAuthenticatedException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotFoundException)
async def handle_not_found(_: Request, exception: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "resource": exception.resource,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(BadGatewayException)
async def handle_bad_gateway(_: Request, exception: BadGatewayException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(InternalServerError)
async def handle_internal_server(_: Request, exception: InternalServerError) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "description": exception.description,
            "details": exception.details,
        },
    )
