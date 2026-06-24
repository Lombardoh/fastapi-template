from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.constants.product_constants import ProductCondition


class ProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    type: str = Field(min_length=1, max_length=50)
    categories: list[str] = Field(min_length=1, max_length=20)
    images: list[str] = Field(default_factory=list, max_length=20)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    quantity: int = Field(ge=0)
    active: bool = True
    sku: str = Field(min_length=1, max_length=80)
    condition: ProductCondition = ProductCondition.NEW
    brand: str | None = Field(default=None, max_length=80)

    @field_validator("name", "type", "sku")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("value cannot be blank")
        return normalized

    @field_validator("categories")
    @classmethod
    def normalize_categories(cls, value: list[str]) -> list[str]:
        categories = [category.strip() for category in value if category.strip()]
        if not categories:
            raise ValueError("categories cannot be empty")
        return categories

    @field_validator("brand")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("images")
    @classmethod
    def normalize_images(cls, value: list[str]) -> list[str]:
        return [image.strip() for image in value if image.strip()]


class ProductCreateRequest(ProductRequest):
    pass


class ProductUpdateRequest(ProductRequest):
    pass
