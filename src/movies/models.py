from __future__ import annotations

import json
from typing import Any, cast, Self

from sqlalchemy import delete, ForeignKey, Integer, select, String, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.movies.exceptions import FavoriteAlreadyExistsException
from src.movies.schemas import MovieData
from src.shared.database import Base


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)

    data: Mapped[str] = mapped_column(String)

    @classmethod
    async def add(cls: type[Movie], db_session: AsyncSession, data: dict[Any, Any]) -> Movie:
        new_movie = Movie(id=data["kinopoiskId"], data=json.dumps(data, ensure_ascii=False))
        db_session.add(new_movie)
        await db_session.flush()
        return new_movie

    @classmethod
    async def get(cls: type[Movie], db_session: AsyncSession, movie_id: int) -> Movie | None:
        query = select(Movie).where(Movie.id == movie_id)
        row = (await db_session.execute(query)).one_or_none()
        if not row:
            return None

        return cast(Movie, row.Movie)


class Favorite(Base):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)

    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))

    __table_args__ = (
        UniqueConstraint("profile_id", "movie_id", name="unique_favorite"),
    )

    async def remove(self: Self, db_session: AsyncSession, movie_id: int, profile_id: int) -> None:
        query = (
            delete(Favorite)
            .where(
                Favorite.profile_id == profile_id,
                Favorite.movie_id == movie_id,
            )
        )
        await db_session.execute(query)

    @classmethod
    async def add(cls: type[Favorite], db_session: AsyncSession, movie_id: int, profile_id: int) -> Favorite:
        new_favorite = Favorite(profile_id=profile_id, movie_id=movie_id)
        db_session.add(new_favorite)
        try:
            await db_session.flush()
        except IntegrityError:
            raise FavoriteAlreadyExistsException from None

        return new_favorite

    @classmethod
    async def get(cls: type[Favorite], db_session: AsyncSession, movie_id: int, profile_id: int) -> Favorite | None:
        query = (
            select(Favorite)
            .where(
                Favorite.profile_id == profile_id,
                Favorite.movie_id == movie_id,
            )
        )
        row = (await db_session.execute(query)).one_or_none()
        if not row:
            return None

        return cast(Favorite, row.Favorite)

    @classmethod
    async def get_all(cls: type[Favorite], db_session: AsyncSession, profile_id: int) -> list[MovieData]:
        query = (
            select(Movie)
            .join_from(
                Favorite, Movie, Favorite.movie_id == Movie.id,
            )
            .where(
                Favorite.profile_id == profile_id,
            )
        )
        rows = (await db_session.execute(query)).all()

        return [MovieData.model_validate(row.Movie, from_attributes=True) for row in rows]
