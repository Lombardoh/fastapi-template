from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Index, String, Table, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.users import User


user_scopes = Table(
    "user_scopes",
    Base.metadata,
    Column(
        "user_id",
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "scope_id",
        PostgresUUID(as_uuid=True),
        ForeignKey("scopes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Scope(BaseModel):
    __tablename__ = "scopes"
    __table_args__ = (
        Index(
            "uq_scopes_name_not_deleted",
            "name",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped[list[User]] = relationship(
        secondary=user_scopes,
        back_populates="scopes",
    )
