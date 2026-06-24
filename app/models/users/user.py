from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.user_constants import UserScope
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.address import Address


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "uq_users_username_not_deleted",
            "username",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
        Index(
            "uq_users_email_not_deleted",
            "email",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    scope: Mapped[UserScope] = mapped_column(
        Enum(
            UserScope,
            name="user_scope",
            native_enum=False,
            values_callable=lambda scopes: [scope.value for scope in scopes],
        ),
        nullable=False,
        default=UserScope.USER,
        server_default=UserScope.USER.value,
    )
    addresses: Mapped[list[Address]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
