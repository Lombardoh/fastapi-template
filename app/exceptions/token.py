from __future__ import annotations

from fastapi import status

from app.constants import DEFAULT_LOCALE
from app.exceptions.base import ApplicationError


class InvalidTokenSecretError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="invalid_token_secret",
            locale=DEFAULT_LOCALE,
        )


class InvalidTokenIssuerError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="invalid_token_issuer",
            locale=DEFAULT_LOCALE,
        )


class InvalidTokenLifetimeError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="invalid_token_lifetime",
            locale=DEFAULT_LOCALE,
        )


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
