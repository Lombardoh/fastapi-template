from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.product_constants import ProductCondition
from app.models.products import Product


class ProductService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: UUID, *, only_active: bool = False) -> Product | None:
        statement = select(Product).where(
            Product.id == product_id,
            Product.deleted_at.is_(None),
        )
        if only_active:
            statement = statement.where(Product.is_active.is_(True))

        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        limit: int,
        offset: int,
        only_active: bool = False,
    ) -> tuple[list[Product], int]:
        statement = self._base_list_statement(only_active=only_active)
        count_statement = select(func.count()).select_from(statement.order_by(None).subquery())

        total_result = await self._session.execute(count_statement)
        total = total_result.scalar_one()

        result = await self._session.execute(
            statement.order_by(Product.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all()), total

    def create(
        self,
        *,
        name: str,
        type: str,
        categories: list[str],
        images: list[str],
        price: Decimal,
        quantity: int,
        is_active: bool,
        sku: str,
        condition: ProductCondition,
        brand: str | None,
    ) -> Product:
        product = Product(
            name=name,
            type=type,
            categories=categories,
            images=images,
            price=price,
            quantity=quantity,
            is_active=is_active,
            sku=sku,
            condition=condition,
            brand=brand,
        )
        self._session.add(product)
        return product

    async def update(
        self,
        product: Product,
        *,
        name: str,
        type: str,
        categories: list[str],
        images: list[str],
        price: Decimal,
        quantity: int,
        is_active: bool,
        sku: str,
        condition: ProductCondition,
        brand: str | None,
    ) -> Product:
        product.name = name
        product.type = type
        product.categories = categories
        product.images = images
        product.price = price
        product.quantity = quantity
        product.is_active = is_active
        product.sku = sku
        product.condition = condition
        product.brand = brand
        await self._session.flush()
        return product

    async def soft_delete(self, product: Product) -> Product:
        product.soft_delete()
        await self._session.flush()
        return product

    def _base_list_statement(self, *, only_active: bool) -> Select[tuple[Product]]:
        statement = select(Product).where(Product.deleted_at.is_(None))
        if only_active:
            statement = statement.where(Product.is_active.is_(True))
        return statement
