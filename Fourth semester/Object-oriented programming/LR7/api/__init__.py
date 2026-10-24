from fastapi import APIRouter
from .routes import router as domain_router

api_router = APIRouter()
api_router.include_router(domain_router, tags=["Food Delivery"])

__all__ = ["api_router"]