from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth.dependencies import get_locale
from app.api.routes.products.dependencies import get_product_service, require_admin_user
from app.db.session import get_session
from app.exceptions.products import ProductNotFoundError
from app.models.users import User
from app.schemas.products import (
    AdminProductResponse,
    AdminProductsPageResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from app.services.products import ProductService

router = APIRouter(
    prefix="/admin/products",
    tags=["admin-products"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("", response_model=AdminProductsPageResponse)
async def list_admin_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> AdminProductsPageResponse:
    products, total = await product_service.list(limit=limit, offset=offset)
    return AdminProductsPageResponse(
        items=[AdminProductResponse.from_product(product) for product in products],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}", response_model=AdminProductResponse)
async def get_admin_product(
    product_id: UUID,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    locale: Annotated[str, Depends(get_locale)],
) -> AdminProductResponse:
    product = await product_service.get_by_id(product_id)
    if product is None:
        raise ProductNotFoundError(locale)
    return AdminProductResponse.from_product(product)


@router.post("", response_model=AdminProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateRequest,
    _admin: Annotated[User, Depends(require_admin_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AdminProductResponse:
    product = product_service.create(
        name=payload.name,
        type=payload.type,
        categories=payload.categories,
        images=payload.images,
        price=payload.price,
        quantity=payload.quantity,
        is_active=payload.active,
        sku=payload.sku,
        condition=payload.condition,
        brand=payload.brand,
    )
    await session.commit()
    await session.refresh(product)
    return AdminProductResponse.from_product(product)


@router.put("/{product_id}", response_model=AdminProductResponse)
async def update_product(
    product_id: UUID,
    payload: ProductUpdateRequest,
    _admin: Annotated[User, Depends(require_admin_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    locale: Annotated[str, Depends(get_locale)],
) -> AdminProductResponse:
    product = await product_service.get_by_id(product_id)
    if product is None:
        raise ProductNotFoundError(locale)

    await product_service.update(
        product,
        name=payload.name,
        type=payload.type,
        categories=payload.categories,
        images=payload.images,
        price=payload.price,
        quantity=payload.quantity,
        is_active=payload.active,
        sku=payload.sku,
        condition=payload.condition,
        brand=payload.brand,
    )
    await session.commit()
    await session.refresh(product)
    return AdminProductResponse.from_product(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    _admin: Annotated[User, Depends(require_admin_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    locale: Annotated[str, Depends(get_locale)],
) -> Response:
    product = await product_service.get_by_id(product_id)
    if product is None:
        raise ProductNotFoundError(locale)

    await product_service.soft_delete(product)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
