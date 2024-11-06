from __future__ import annotations

from fastapi import status

from src.shared.exceptions import BadRequestException, NotAllowedException, NotAuthenticatedException, NotFoundException


class ProfileNotFoundException(NotFoundException):
    resource: str = "Profile"

    description = "No profile matches provided credentials."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class DuplicateProfileException(BadRequestException):
    action = "Create profile"

    description = "Profile already exists."
    details: str = "There is another profile with same value for one of the unique fields."
    status_code = status.HTTP_400_BAD_REQUEST


class ExpiredTokenException(NotAuthenticatedException):
    description = "Request initiator's token is expired."
    details = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenException(NotAllowedException):
    action = "Authorization"

    description = "Invalid token."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN
