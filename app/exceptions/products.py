from __future__ import annotations

from fastapi import status

from app.exceptions.base import ApplicationError


class ProductNotFoundError(ApplicationError):
    def __init__(self, locale: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="product_not_found",
            locale=locale,
        )
