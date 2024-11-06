from __future__ import annotations

from typing import Annotated, TYPE_CHECKING  # noqa: TCH003

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # noqa: TCH002
from jwt.exceptions import InvalidSignatureError

from src.auth.exceptions import InvalidTokenException, ProfileNotFoundException
from src.auth.models import Profile
from src.auth.schemas import TokenPayload
from src.shared.database import get_session


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


bearer = HTTPBearer(description="JWT access token.")


async def get_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db_session: AsyncSession = Depends(get_session),
) -> TokenPayload:
    """Validate authorization token."""
    try:
        payload = TokenPayload.from_token(token.credentials)
    except InvalidSignatureError:
        raise InvalidTokenException from None

    if not await Profile.get_profile(db_session=db_session, profile_id=payload.profile_id):
        raise ProfileNotFoundException

    return payload
