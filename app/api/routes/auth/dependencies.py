from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.config_constants import AVAILABLE_LOCALES, DEFAULT_LOCALE
from app.core.config import settings
from app.db.session import get_session
from app.exceptions.token import InvalidAccessTokenError
from app.exceptions.users import InactiveUserError, UserNotFoundError
from app.models.users import User
from app.services.auth import AuthService
from app.services.token_service import TokenService
from app.services.users import UserService
from app.services.users.passwords import PasswordService


def get_locale(accept_language: Annotated[str | None, Header()] = None) -> str:
    if accept_language is None:
        return DEFAULT_LOCALE

    for language in accept_language.split(","):
        locale = language.split(";", 1)[0].strip().replace("-", "_")
        if locale in AVAILABLE_LOCALES:
            return locale

    return DEFAULT_LOCALE


def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.token_secret_key,
        issuer=settings.token_issuer,
        access_token_lifetime=timedelta(minutes=settings.access_token_lifetime_minutes),
    )


def get_password_service() -> PasswordService:
    return PasswordService()


def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
) -> AuthService:
    return AuthService(session, token_service, password_service)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    locale: Annotated[str, Depends(get_locale)],
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    if authorization is None:
        raise InvalidAccessTokenError(locale)

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise InvalidAccessTokenError(locale)

    user_id = token_service.decode_access_token(token, locale)
    user = await UserService(session).get_by_id(user_id)
    if user is None:
        raise UserNotFoundError(locale)
    if not user.is_active:
        raise InactiveUserError(locale)

    return user
