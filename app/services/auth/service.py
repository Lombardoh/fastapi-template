from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.users import InactiveUserError, InvalidCredentialsError, UserAlreadyExistsError
from app.models.users import User
from app.services.token_service import TokenService
from app.services.users import UserService
from app.services.users.passwords import PasswordService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        token_service: TokenService,
        password_service: PasswordService,
    ) -> None:
        self._session = session
        self._users = UserService(session)
        self._tokens = token_service
        self._passwords = password_service

    async def register(self, email: str, password: str, locale: str) -> tuple[User, str]:
        existing_user = await self._users.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError(locale)

        user = self._users.create(
            email=email,
            password_hash=self._passwords.hash_password(password),
        )

        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise UserAlreadyExistsError(locale) from exc

        created_user = await self._users.get_by_id(user.id)
        if created_user is None:
            raise InvalidCredentialsError(locale)

        return created_user, self._tokens.create_access_token(created_user.id)

    async def login(self, email: str, password: str, locale: str) -> tuple[User, str]:
        user = await self._users.get_by_email(email)
        if user is None or not self._passwords.verify_password(password, user.password):
            raise InvalidCredentialsError(locale)

        if not user.is_active:
            raise InactiveUserError(locale)

        return user, self._tokens.create_access_token(user.id)
