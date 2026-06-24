from fastapi import APIRouter

from app.api.routes.products import admin, public

router = APIRouter()
router.include_router(public.router)
router.include_router(admin.router)

__all__ = ["router"]
