from aiogram import Router

from app.handlers.catalog import router as catalog_router
from app.handlers.cart import router as cart_router
from app.handlers.order import router as order_router
from app.handlers.weather import router as weather_router
from app.handlers.admin import router as admin_router

router = Router()

router.include_router(catalog_router)
router.include_router(cart_router)
router.include_router(order_router)
router.include_router(weather_router)
router.include_router(admin_router)

__all__ = ['router']