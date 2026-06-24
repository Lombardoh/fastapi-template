from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.users import User


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(User)
            .options(selectinload(User.scopes))
            .where(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User)
            .options(selectinload(User.scopes))
            .where(
                User.email == email,
                User.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password=password_hash)
        self._session.add(user)
        return user
