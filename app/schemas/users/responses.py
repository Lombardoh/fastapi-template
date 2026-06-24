from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.users import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    is_active: bool
    scopes: list[str]

    @classmethod
    def from_user(cls, user: User) -> UserResponse:
        return cls(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            scopes=[scope.name for scope in user.scopes],
        )
