from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# we choose not to parse kinopoisk data and simply hamfist all of it into db as string
# such a solution only came about because there is a pretty tight time constraint for that app's development
class MovieData(BaseModel):
    data: Any


class Movie(BaseModel):
    id: int = Field(examples=[301])


class Movies(BaseModel):
    movies: list[MovieData]
