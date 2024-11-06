from __future__ import annotations

from fastapi import status

from src.shared.exceptions import BadRequestException, NotFoundException


class FavoriteAlreadyExistsException(BadRequestException):
    action = "Add favorite"

    description = "Movie is already in favorites."
    details: str = "Movie with provided id is present in current user's favorite list."
    status_code = status.HTTP_400_BAD_REQUEST


class FavoriteNotFoundException(NotFoundException):
    resource = "Favorite"

    description = "Request is not correct."
    details = "Could not find favorite relation with provided data."
    status_code = status.HTTP_400_BAD_REQUEST
