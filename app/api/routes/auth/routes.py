from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.routes.auth.dependencies import get_auth_service, get_current_user, get_locale
from app.models.users import User
from app.schemas.auth import AuthResponse, LoginRequest, ProfileResponse, RegisterRequest
from app.schemas.users import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    locale: Annotated[str, Depends(get_locale)],
) -> AuthResponse:
    user, access_token = await auth_service.register(payload.email, payload.password, locale)
    return AuthResponse(access_token=access_token, user=UserResponse.from_user(user))


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    locale: Annotated[str, Depends(get_locale)],
) -> AuthResponse:
    user, access_token = await auth_service.login(payload.email, payload.password, locale)
    return AuthResponse(access_token=access_token, user=UserResponse.from_user(user))


@router.get("/me", response_model=ProfileResponse)
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> ProfileResponse:
    return ProfileResponse(user=UserResponse.from_user(current_user))
