from __future__ import annotations

from pydantic import BaseModel

from app.schemas.users import UserResponse


class ProfileResponse(BaseModel):
    user: UserResponse


class AuthResponse(ProfileResponse):
    access_token: str
    token_type: str = "bearer"
