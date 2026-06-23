from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError

from app.exceptions.token import (
    InvalidAccessTokenError,
    InvalidAccessTokenSubjectError,
    InvalidAccessTokenTypeError,
    InvalidTokenIssuerError,
    InvalidTokenLifetimeError,
    InvalidTokenSecretError,
)


class TokenService:
    algorithm = "HS256"

    def __init__(
        self,
        secret_key: str,
        issuer: str,
        access_token_lifetime: timedelta,
    ) -> None:
        if not secret_key:
            raise InvalidTokenSecretError
        if not issuer:
            raise InvalidTokenIssuerError
        if access_token_lifetime <= timedelta(0):
            raise InvalidTokenLifetimeError

        self._secret_key = secret_key
        self._issuer = issuer
        self._access_token_lifetime = access_token_lifetime

    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(UTC)
        return jwt.encode(
            {
                "sub": str(user_id),
                "iss": self._issuer,
                "iat": now,
                "exp": now + self._access_token_lifetime,
                "type": "access",
            },
            self._secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(self, token: str, locale: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self.algorithm],
                issuer=self._issuer,
                options={
                    "require": ["sub", "iss", "iat", "exp", "type"],
                },
            )
        except PyJWTInvalidTokenError as exc:
            raise InvalidAccessTokenError(locale) from exc

        if payload["type"] != "access":
            raise InvalidAccessTokenTypeError(locale)

        try:
            return UUID(payload["sub"])
        except (TypeError, ValueError) as exc:
            raise InvalidAccessTokenSubjectError(locale) from exc
