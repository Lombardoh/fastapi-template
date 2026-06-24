from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.constants.product_constants import ProductCondition
from app.models.products import Product


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    type: str
    categories: list[str]
    images: list[str]
    price: Decimal
    quantity: int
    condition: ProductCondition
    brand: str | None

    @classmethod
    def from_product(cls, product: Product) -> ProductResponse:
        return cls(
            id=product.id,
            name=product.name,
            type=product.type,
            categories=product.categories,
            images=product.images,
            price=product.price,
            quantity=product.quantity,
            condition=product.condition,
            brand=product.brand,
        )


class AdminProductResponse(ProductResponse):
    active: bool
    sku: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    @classmethod
    def from_product(cls, product: Product) -> AdminProductResponse:
        return cls(
            id=product.id,
            name=product.name,
            type=product.type,
            categories=product.categories,
            images=product.images,
            price=product.price,
            quantity=product.quantity,
            condition=product.condition,
            brand=product.brand,
            active=product.is_active,
            sku=product.sku,
            created_at=product.created_at,
            updated_at=product.updated_at,
            deleted_at=product.deleted_at,
        )


class ProductsPageResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    limit: int
    offset: int


class AdminProductsPageResponse(BaseModel):
    items: list[AdminProductResponse]
    total: int
    limit: int
    offset: int
