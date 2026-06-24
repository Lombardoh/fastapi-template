from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.scope import user_scopes

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.scope import Scope


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "uq_users_email_not_deleted",
            "email",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    scopes: Mapped[list[Scope]] = relationship(
        secondary=user_scopes,
        back_populates="users",
    )
    addresses: Mapped[list[Address]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
