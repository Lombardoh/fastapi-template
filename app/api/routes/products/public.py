from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.routes.auth.dependencies import get_locale
from app.api.routes.products.dependencies import get_product_service
from app.exceptions.products import ProductNotFoundError
from app.schemas.products import ProductResponse, ProductsPageResponse
from app.services.products import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductsPageResponse)
async def list_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ProductsPageResponse:
    products, total = await product_service.list(limit=limit, offset=offset, only_active=True)
    return ProductsPageResponse(
        items=[ProductResponse.from_product(product) for product in products],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    locale: Annotated[str, Depends(get_locale)],
) -> ProductResponse:
    product = await product_service.get_by_id(product_id, only_active=True)
    if product is None:
        raise ProductNotFoundError(locale)
    return ProductResponse.from_product(product)
