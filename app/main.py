"""
FastAPI 应用工厂与启动入口
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.core.middleware import RequestIDMiddleware, AccessLogMiddleware
from app.api.v1.router import api_router

# 优先初始化日志，后续所有模块均从 logging 标准库获取 logger
setup_logging()
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# OpenAPI Tags 元数据
# --------------------------------------------------------------------------- #
OPENAPI_TAGS = [
    {
        "name": "Root",
        "description": "服务根路径，返回基本服务信息。",
    },
    {
        "name": "Health",
        "description": "健康检查接口。\n\n"
                        "- **GET /health** — 存活探针（Liveness），确认进程仍在运行。\n"
                        "- **GET /health/ready** — 就绪探针（Readiness），确认服务已完成初始化并可接收流量。",
    },
    {
        "name": "Agent",
        "description": "AI Agent 相关接口。\n\n"
                        "目前提供基于 `agent-framework` 的**计算器工作流**示例，"
                        "演示 Fan-Out / Fan-In 多步骤 Agent 编排模式。",
    },
    {
        "name": "Demo",
        "description": "演示接口，展示统一响应格式、分页、参数校验及业务异常处理等典型用法。",
    },
]


# --------------------------------------------------------------------------- #
# 生命周期
# --------------------------------------------------------------------------- #
@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    logger.info("=" * 60)
    logger.info(f"  {settings.APP_NAME}  v{settings.APP_VERSION}  启动中...")
    logger.info(f"  环境: {settings.ENVIRONMENT}  |  调试: {settings.DEBUG}")
    logger.info("=" * 60)
    yield
    logger.info(f"{settings.APP_NAME} 已关闭。")


# --------------------------------------------------------------------------- #
# 应用实例
# --------------------------------------------------------------------------- #
def create_app() -> FastAPI:
    fast_app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=OPENAPI_TAGS,
        contact={
            "name": "Agent API Team",
        },
        license_info={
            "name": "MIT",
        },
    )

    # ---- 中间件（注意：后注册先执行） ----
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    fast_app.add_middleware(AccessLogMiddleware)   # 记录请求 / 响应日志
    fast_app.add_middleware(RequestIDMiddleware)   # 为每个请求注入 X-Request-ID

    # ---- 全局异常处理 ----
    setup_exception_handlers(fast_app)

    # ---- 路由 ----
    fast_app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # ---- 根路由 ----
    @fast_app.get("/", tags=["Root"])
    async def root():
        return {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    return fast_app


app = create_app()
