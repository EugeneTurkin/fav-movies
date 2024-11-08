from __future__ import annotations

from fastapi import status


class HTTPException(Exception):
    """Base class for all app exceptions."""

    description = "Unknown error occured."
    details = "Please contact backend maintenance team."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NotAuthenticatedException(HTTPException):
    """Exception for 401 UNAUTHORIZED error."""

    description = "Request initiator is not authenticated."
    details = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class NotFoundException(HTTPException):
    """Exception for 404 NOT FOUND error."""

    resource: str

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class NotAllowedException(HTTPException):
    """Exception for 403 FORBIDDEN error."""

    action: str

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class BadRequestException(HTTPException):
    """Exception for 400 BAD REQUEST error."""

    action: str

    description = "Request is not correct."
    details = "Request is not correct and cannot be handled."
    status_code = status.HTTP_400_BAD_REQUEST


class BadGatewayException(HTTPException):
    """Exception for 502 BAD GATEWAY error."""

    description = "Failed to establish a connection to an upstream server."
    details = "Connection could not be established due to missing requirements."
    status_code = status.HTTP_502_BAD_GATEWAY


class InternalServerError(HTTPException):
    """Exception for 500 INTERNAL SERVER ERROR error."""

    description = "Unexpected error while dealing with an upstream."
    details = "Unhandled response from a remote server."
    status_code = status.HTTP_502_BAD_GATEWAY
