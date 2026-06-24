from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, Enum, Index, Integer, Numeric, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.product_constants import ProductCondition
from app.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    __table_args__ = (
        Index(
            "uq_products_sku_not_deleted",
            "sku",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    categories: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    images: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
        index=True,
    )
    sku: Mapped[str] = mapped_column(String(80), nullable=False)
    condition: Mapped[ProductCondition] = mapped_column(
        Enum(
            ProductCondition,
            name="product_condition",
            native_enum=False,
            values_callable=lambda conditions: [condition.value for condition in conditions],
        ),
        nullable=False,
        default=ProductCondition.NEW,
        server_default=ProductCondition.NEW.value,
    )
    brand: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
