from __future__ import annotations

import hashlib
import typing
import uuid
from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, select, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.enums import Encoding, HashingAlgorithm
from src.auth.exceptions import DuplicateProfileException, ProfileNotFoundException
from src.auth.schemas import Credentials
from src.shared.database import Base
from src.shared.datetime import utcnow


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    password_hash: Mapped["PasswordHash"] = relationship(uselist=False, back_populates="profile")  # noqa: UP037

    @classmethod
    async def get_profile(cls: type[Profile], db_session: AsyncSession, profile_id: int) -> Profile:
        query = select(Profile).where(Profile.id == profile_id)
        row = (await db_session.execute(query)).one_or_none()

        if not row:
            raise ProfileNotFoundException

        return typing.cast(Profile, row.Profile)

    @classmethod
    async def get_by_credentials(cls: type[Profile], credentials: Credentials, db_session: AsyncSession) -> Profile:
        query = (
            select(Profile, PasswordHash)
            .join(PasswordHash, Profile.id == PasswordHash.profile_id)
            .where(Profile.name == credentials.name)
        )
        row = (await db_session.execute(query)).one_or_none()

        if row is None or not row.PasswordHash.check(credentials.password):
            raise ProfileNotFoundException

        return typing.cast(Profile, row.Profile)

    @classmethod
    async def register(cls: type[Profile], credentials: Credentials, db_session: AsyncSession) -> Profile:
        new_profile = Profile(name=credentials.name)
        db_session.add(new_profile)
        try:
            await db_session.flush()
        except IntegrityError:
            raise  DuplicateProfileException from None

        await PasswordHash.new_object(db_session, credentials.password, new_profile.id)

        return new_profile


class PasswordHash(Base):
    __tablename__ = "password_hash"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), primary_key=True)

    algorithm: Mapped[HashingAlgorithm] = mapped_column(Enum(HashingAlgorithm, name="hashing_algorithm_enum"),
                                                        nullable=False)
    salt: Mapped[str] = mapped_column(String(36), nullable=False)
    value: Mapped[str] = mapped_column(String(128), nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="password_hash")  # noqa: UP037

    def _generate_hash(self: Self, password: str) -> str:
        salted_input = password + self.salt
        hash_object = hashlib.new(self.algorithm.value)
        hash_object.update(salted_input.encode(Encoding.ASCII.value))
        return hash_object.hexdigest()

    def _hash_password(self: Self, password: str) -> None:
        self.salt = str(uuid.uuid4())
        self.algorithm = HashingAlgorithm.SHA256
        self.value = self._generate_hash(password)

    def check(self: Self, password: str) -> bool:
        password_hash = self._generate_hash(password)
        return password_hash == self.value

    @classmethod
    async def new_object(
        cls: type[PasswordHash],
        db_session: AsyncSession,
        password: str,
        profile_id: int,
    ) -> PasswordHash:
        new_password_hash = PasswordHash(profile_id=profile_id)
        new_password_hash._hash_password(password)  # noqa: SLF001
        db_session.add(new_password_hash)
        await db_session.flush()
        return new_password_hash
