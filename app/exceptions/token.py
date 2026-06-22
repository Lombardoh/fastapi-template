from __future__ import annotations

from fastapi import status

from app.exceptions.base import ApplicationError


class InvalidAccessTokenError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_access_token",
            locale=locale,
        )


class InvalidAccessTokenTypeError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_access_token_type",
            locale=locale,
        )


class InvalidAccessTokenSubjectError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_access_token_subject",
            locale=locale,
        )
