from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth.dependencies import get_current_user, get_locale
from app.constants.user_constants import UserScope
from app.db.session import get_session
from app.exceptions.base import ApplicationError
from app.models.users import User
from app.services.products import ProductService


def get_product_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductService:
    return ProductService(session)


async def require_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
    locale: Annotated[str, Depends(get_locale)],
) -> User:
    if current_user.scope != UserScope.ADMIN:
        raise ApplicationError(status_code=403, code="forbidden", locale=locale)
    return current_user
