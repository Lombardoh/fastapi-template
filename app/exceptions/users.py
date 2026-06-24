from __future__ import annotations

from fastapi import status

from app.exceptions.base import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="user_already_exists",
            locale=locale,
        )


class UserNotFoundError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="user_not_found",
            locale=locale,
        )


class InvalidCredentialsError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            locale=locale,
        )


class InactiveUserError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="inactive_user",
            locale=locale,
        )
