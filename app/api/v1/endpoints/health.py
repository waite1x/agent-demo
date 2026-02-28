"""
健康检查端点
GET /api/v1/health      - 基本存活检测
GET /api/v1/health/ready - 就绪检测（可扩展数据库 / 缓存连通性）
"""
import logging
import time

from fastapi import APIRouter
from app.schemas.response import ApiResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# 记录服务启动时间
_START_TIME = time.time()


@router.get("", summary="存活检测 (Liveness)")
async def liveness():
    logger.debug("liveness probe ok")
    return ApiResponse.ok(data={"status": "alive"}, message="服务运行中")


@router.get("/ready", summary="就绪检测 (Readiness)")
async def readiness():
    uptime_seconds = int(time.time() - _START_TIME)
    logger.debug(f"readiness probe ok | uptime={uptime_seconds}s")
    return ApiResponse.ok(
        data={
            "status": "ready",
            "uptime_seconds": uptime_seconds,
        },
        message="服务就绪",
    )
