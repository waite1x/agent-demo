"""
自定义中间件
- RequestIDMiddleware : 为每个请求注入唯一 X-Request-ID
- AccessLogMiddleware : 记录请求耗时、状态码等访问日志
"""
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    为每个请求生成并传递唯一 Request ID。
    - 若客户端已提供 X-Request-ID 则沿用，否则自动生成 UUID4。
    - 在响应头中回传 X-Request-ID。
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        # 将 request_id 存入 request.state 供后续中间件 / 路由使用
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class AccessLogMiddleware(BaseHTTPMiddleware):
    """
    记录每次 HTTP 请求的访问日志：
      方法、路径、状态码、耗时、客户端 IP
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        method = request.method
        path = request.url.path
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or (request.client.host if request.client else "unknown")
        )
        request_id = getattr(request.state, "request_id", "-")

        try:
            response = await call_next(request)
            elapsed_ms = (time.perf_counter() - start) * 1000
            status_code = response.status_code

            log_fn = logger.info if status_code < 400 else logger.warning
            log_fn(
                f'{client_ip} | {method} {path} | {status_code} | {elapsed_ms:.1f}ms | rid={request_id}'
            )
            return response

        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.error(
                f'{client_ip} | {method} {path} | 500 | {elapsed_ms:.1f}ms | rid={request_id} | {exc}'
            )
            raise
