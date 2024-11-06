from __future__ import annotations

from datetime import datetime, timedelta
from typing import Self

import jwt
from pydantic import BaseModel, Field

from src.auth.enums import SignatureAlgorithm
from src.auth.exceptions import ExpiredTokenException
from src.config import CONFIG
from src.shared.datetime import utcnow


class Credentials(BaseModel):
    name: str = Field(min_length=5, max_length=100, examples=["example_username"])
    password: str = Field(min_length=10, max_length=200, examples=["Examplepassword123"])


class ProfileData(BaseModel):
    id: int

    name: str = Field(min_length=5, max_length=100, examples=["example_username"])
    created_at: datetime


class Token(BaseModel):
    """JWT authorization token."""

    token: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJwcm9maWxlX2lkIjoxLCJleHAiOjE3MzA4NDI0ODB9"
            ".oa9-E68yqut10wx9CoXENPc-ArjUuIVmoD42hFFxRxY",
        ],
    )


class TokenPayload(BaseModel):
    profile_id: int

    @classmethod
    def from_token(cls: type[TokenPayload], token: str) -> TokenPayload:
        """Decode JWT token into a class instance."""
        try:
            payload_dict = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[SignatureAlgorithm.HS256.value])
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException from None

        return TokenPayload.model_validate(payload_dict)

    @property
    def token(self: Self) -> str:
        """Encode data into JWT token."""
        payload_data = {
            "profile_id": self.profile_id,
            "exp": utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(payload_data, CONFIG.SECRET_KEY, SignatureAlgorithm.HS256.value)
