from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import controllers
from src.auth.dependencies import get_token
from src.auth.schemas import Credentials, ProfileData, Token, TokenPayload
from src.shared.database import get_session
from src.shared.exc_responses import responses


router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    description="Register by creating a new profile.",
    responses={
        status.HTTP_201_CREATED: {"description": "New profile created."},
        status.HTTP_400_BAD_REQUEST: {"description": "Duplicate profile credentials provided."},
    },
    response_model=ProfileData,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    credentials: Annotated[Credentials, Body()],
    db_session: AsyncSession = Depends(get_session),
) -> ProfileData:
    return await controllers.register(credentials, db_session)


@router.post(
    "/login",
    description="Login by entreing credentials and recieve JWT authorization token.",
    responses={
        status.HTTP_201_CREATED: {"description": "Login - bearer token is created."},
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def login(
    credentials: Annotated[Credentials, Body()],
    db_session: AsyncSession = Depends(get_session),
) -> Token:
    return await controllers.login(credentials, db_session)


@router.get(
    "/profile",
    description="Get current user's profile data.",
    responses={
        status.HTTP_200_OK: {"description": "Get Profile - get token's owner profile data."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=ProfileData,
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    db_session: AsyncSession = Depends(get_session),
    token: TokenPayload = Depends(get_token),
) -> ProfileData:
    return await controllers.get_profile(db_session, token)
