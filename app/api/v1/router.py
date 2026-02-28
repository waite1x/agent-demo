"""
API v1 路由聚合
"""
from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.demo import router as demo_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(demo_router,  prefix="/demo",   tags=["Demo"])
