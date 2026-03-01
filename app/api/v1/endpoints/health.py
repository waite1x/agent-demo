"""
健康检查端点
GET /api/v1/health      - 基本存活检测
GET /api/v1/health/ready - 就绪检测（可扩展数据库 / 缓存连通性）
"""
import logging
import time

from app.core.routing import AppAPIRouter
from app.schemas.response import ApiResponse

logger = logging.getLogger(__name__)

TAG_META = {
    "name": "Health",
    "description": "健康检查接口。\n\n"
                   "- **GET /health** — 存活探针（Liveness），确认进程仍在运行。\n"
                   "- **GET /health/ready** — 就绪探针（Readiness），确认服务已完成初始化并可接收流量。",
}

router = AppAPIRouter(tags=["Health"])

# 记录服务启动时间
_START_TIME = time.time()


@router.get(
    "",
    response_model=ApiResponse,
    responses={200: {"description": "服务运行中"}},
)
async def liveness():
    """存活检测 (Liveness)

    确认进程仍在运行，适用于 Kubernetes liveness probe。
    """
    logger.debug("liveness probe ok")
    return ApiResponse.ok(data={"status": "alive"}, message="服务运行中")


@router.get(
    "/ready",
    response_model=ApiResponse,
    responses={200: {"description": "服务就绪"}},
)
async def readiness():
    """就绪检测 (Readiness)

    确认服务已完成初始化并可接收流量，适用于 Kubernetes readiness probe。
    """
    uptime_seconds = int(time.time() - _START_TIME)
    logger.debug(f"readiness probe ok | uptime={uptime_seconds}s")
    return ApiResponse.ok(
        data={
            "status": "ready",
            "uptime_seconds": uptime_seconds,
        },
        message="服务就绪",
    )

