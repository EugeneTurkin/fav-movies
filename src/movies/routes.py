from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.movies import controllers
from src.movies.schemas import Movie, MovieData, Movies
from src.shared.database import get_session
from src.shared.exc_responses import responses


router = APIRouter(tags=["movies"])


@router.get(
    "/movies/favorites",
    description="Get favorites - get a list of current user's favorite movies data.",
    responses={
        status.HTTP_200_OK: {"description": "List of current user's favorite movies data is returned."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=Movies,
    status_code=status.HTTP_200_OK,
)
async def get_favorites(
    db_session: AsyncSession = Depends(get_session),
    token: TokenPayload = Depends(get_token),
) -> Movies:
    return await controllers.get_favorites(db_session, token)


@router.post(
    "/movies/favorites",
    description="Add favoite - request movie data, save it to DB and add movie to current user's favorites list. ",
    responses={
        status.HTTP_200_OK: {"description": "Movie added to current user's favorite list and data is returned."},
        status.HTTP_400_BAD_REQUEST: {"description": "Movie already in current user's favorites."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: responses[status.HTTP_500_INTERNAL_SERVER_ERROR],
        status.HTTP_502_BAD_GATEWAY: responses[status.HTTP_502_BAD_GATEWAY],
    },
    response_model=MovieData,
    status_code=status.HTTP_200_OK,
)
async def add_favourite(
    movie: Annotated[Movie, Body()],
    db_session: AsyncSession = Depends(get_session),
    token: TokenPayload = Depends(get_token),
) -> MovieData:
    return await controllers.add_favourite(movie, db_session, token)


@router.get(
    "/movies/search",
    description="Search movie by keyword.",
    responses={
        status.HTTP_200_OK: {"description": "List of movies' data is returned."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: responses[status.HTTP_500_INTERNAL_SERVER_ERROR],
        status.HTTP_502_BAD_GATEWAY: responses[status.HTTP_502_BAD_GATEWAY],
    },
    response_model=MovieData,
    status_code=status.HTTP_200_OK,
)
async def movie_search_by_keyword(
    keyword: Annotated[str, Query(example="мстители")],
    token: TokenPayload = Depends(get_token),  # noqa: ARG001
) -> MovieData:
    return await controllers.movie_search_by_keyword(keyword)


@router.get(
    "/movies/{kinopoisk_id}",
    description="Search movie by id.",
    responses={
        status.HTTP_200_OK: {"description": "Movie with provided id is returned."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: responses[status.HTTP_500_INTERNAL_SERVER_ERROR],
        status.HTTP_502_BAD_GATEWAY: responses[status.HTTP_502_BAD_GATEWAY],
    },
    response_model=MovieData,
    status_code=status.HTTP_200_OK,
)
async def movie_search_by_id(
    kinopoisk_id: Annotated[int, Path(example=301)],
    token: TokenPayload = Depends(get_token),  # noqa: ARG001
) -> MovieData:
    return await controllers.movie_search_by_id(kinopoisk_id=kinopoisk_id)


@router.delete(
    "/movies/favorites/{kinopoisk_id}",
    description="Remove movie from current user's favorites list.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Movie is removed from current user's favorites list."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_favorite(
    kinopoisk_id: Annotated[int, Path(example=301)],
    db_session: AsyncSession = Depends(get_session),
    token: TokenPayload = Depends(get_token),
) -> None:
    await controllers.remove_favorite(kinopoisk_id=kinopoisk_id, db_session=db_session, token=token)
