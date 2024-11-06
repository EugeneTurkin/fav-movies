from __future__ import annotations

from typing import TYPE_CHECKING

from src.auth.models import Profile
from src.auth.schemas import ProfileData, Token, TokenPayload


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.schemas import Credentials


async def register(credentials: Credentials, db_session: AsyncSession) -> ProfileData:
    profile = await Profile.register(credentials=credentials, db_session=db_session)

    return ProfileData.model_validate(profile, from_attributes=True)


async def login(credentials: Credentials, db_session: AsyncSession) -> Token:
    profile = await Profile.get_by_credentials(credentials=credentials, db_session=db_session)

    token_payload = TokenPayload(profile_id=profile.id)

    return Token(token=token_payload.token)


async def get_profile(db_session: AsyncSession, token: TokenPayload) -> ProfileData:
    profile = await Profile.get_profile(db_session=db_session, profile_id=token.profile_id)

    return ProfileData.model_validate(profile, from_attributes=True)
