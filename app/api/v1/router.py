"""
API v1 路由聚合
"""
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.demo import router as demo_router
from app.api.v1.endpoints.agent import router as agent_router

api_router = APIRouter()

# 公开路由
api_router.include_router(health_router, prefix="/health")

# 需要 JWT 认证的路由
_auth = [Depends(get_current_user)]
api_router.include_router(agent_router, prefix="/agent", dependencies=_auth)
api_router.include_router(demo_router,  prefix="/demo",  dependencies=_auth)
