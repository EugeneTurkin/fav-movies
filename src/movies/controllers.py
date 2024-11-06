from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp

from src.movies.enums import KPResponse
from src.movies.exceptions import FavoriteNotFoundException
from src.movies.models import Favorite, Movie
from src.movies.schemas import MovieData, Movies
from src.movies.utlis import headers, kinopoisk_unoff_base_url
from src.shared.exceptions import BadGatewayException, InternalServerError


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.schemas import TokenPayload
    from src.movies.schemas import Movie as MovieSchema


async def get_favorites(db_session: AsyncSession, token: TokenPayload) -> Movies:
    movies = await Favorite.get_all(db_session, token.profile_id)

    return Movies(movies=movies)


async def add_favourite(movie: MovieSchema, db_session: AsyncSession, token: TokenPayload) -> MovieData:
    movie_obj = await Movie.get(db_session=db_session, movie_id=movie.id)
    if not movie_obj:
        data = (await movie_search_by_id(movie.id)).data
        movie_obj = await Movie.add(db_session=db_session, data=data)

    await Favorite.add(db_session, movie_obj.id, token.profile_id)
    return MovieData(data=movie_obj.data)


async def movie_search_by_keyword(keyword: str) -> MovieData:
    async with aiohttp.ClientSession(headers=headers) as session:  # noqa: SIM117
        async with session.get(
            kinopoisk_unoff_base_url + "/v2.1/films/search-by-keyword",
            params={"keyword": keyword},
        ) as resp:
            if resp.status == KPResponse.UNATHORIZED.value:
                raise BadGatewayException
            if resp.status != KPResponse.OK.value:
                raise InternalServerError
            return MovieData(data=await resp.json())


async def movie_search_by_id(kinopoisk_id: int) -> MovieData:
    async with aiohttp.ClientSession(headers=headers) as session:  # noqa: SIM117
        async with session.get(f"{kinopoisk_unoff_base_url}/v2.2/films/{kinopoisk_id}") as resp:
            if resp.status == KPResponse.UNATHORIZED.value:
                raise BadGatewayException
            if resp.status != KPResponse.OK.value:
                raise InternalServerError
            return MovieData(data=await resp.json())


async def remove_favorite(kinopoisk_id: int, db_session: AsyncSession, token: TokenPayload) -> None:
    fav = await Favorite.get(db_session, kinopoisk_id, token.profile_id)
    if not fav:
        raise FavoriteNotFoundException

    await fav.remove(db_session, kinopoisk_id, token.profile_id)
