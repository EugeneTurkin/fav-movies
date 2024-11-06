from __future__ import annotations

from fastapi import status

from src.shared import exceptions, schemas


responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Provided tokens or credentials are invalid or missing.",
        "model": schemas.NotAuthenticatedResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": exceptions.NotAuthenticatedException.description,
                    "details": exceptions.NotAuthenticatedException.details,
                },
            },
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Provided tokens or credentials don't grant you enough access rights.",
        "model": schemas.NotAllowedResponse,
        "content": {
            "application/json": {
                "example": {
                    "action": "<requested action description will be here>",
                    "description": exceptions.NotAllowedException.description,
                    "details": exceptions.NotAllowedException.details,
                },
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Requested resource doesn't exist.",
        "model": schemas.NotFoundResponse,
        "content": {
            "application/json": {
                "example": {
                    "resource": "<requested resource description will be here>",
                    "description": exceptions.NotFoundException.description,
                    "details": exceptions.NotFoundException.details,
                },
            },
        },
    },
    status.HTTP_502_BAD_GATEWAY: {
        "description": "Failed to connect to a remote server.",
        "model": schemas.BadGatewayResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": exceptions.BadGatewayException.description,
                    "details": exceptions.BadGatewayException.details,
                },
            },
        },
    },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Unexpected error while handling response from a remote server.",
        "model": schemas.InternalServerResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": exceptions.InternalServerError.description,
                    "details": exceptions.InternalServerError.details,
                },
            },
        },
    },
}
