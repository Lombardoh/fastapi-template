from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.constants.user_constants import UserScope
from app.models.users import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    is_active: bool
    scope: UserScope

    @classmethod
    def from_user(cls, user: User) -> UserResponse:
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            scope=user.scope,
        )
