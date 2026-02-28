"""
全局异常处理
- 自定义业务异常 AppException
- HTTP 异常、请求校验异常、未捕获异常的统一响应格式
"""
import logging
import traceback
from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# 自定义异常体系
# --------------------------------------------------------------------------- #
class AppException(Exception):
    """业务异常基类"""

    def __init__(
        self,
        code: int = 40000,
        message: str = "业务错误",
        data: Optional[Any] = None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.code = code
        self.message = message
        self.data = data
        self.http_status = http_status
        super().__init__(message)


class NotFoundError(AppException):
    """资源不存在"""
    def __init__(self, message: str = "资源不存在", data: Optional[Any] = None):
        super().__init__(code=40400, message=message, data=data,
                         http_status=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppException):
    """未认证"""
    def __init__(self, message: str = "未认证，请先登录", data: Optional[Any] = None):
        super().__init__(code=40100, message=message, data=data,
                         http_status=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    """无权限"""
    def __init__(self, message: str = "无访问权限", data: Optional[Any] = None):
        super().__init__(code=40300, message=message, data=data,
                         http_status=status.HTTP_403_FORBIDDEN)


class InternalServerError(AppException):
    """服务器内部错误"""
    def __init__(self, message: str = "服务器内部错误", data: Optional[Any] = None):
        super().__init__(code=50000, message=message, data=data,
                         http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------------------------------------------------------------- #
# 统一响应格式辅助
# --------------------------------------------------------------------------- #
def _error_response(
    request: Request,
    http_status: int,
    code: int,
    message: str,
    data: Optional[Any] = None,
) -> JSONResponse:
    request_id = request.headers.get("X-Request-ID", "-")
    return JSONResponse(
        status_code=http_status,
        content={
            "success": False,
            "code": code,
            "message": message,
            "data": data,
            "request_id": request_id,
        },
    )


# --------------------------------------------------------------------------- #
# 异常处理器
# --------------------------------------------------------------------------- #
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(
        f"[AppException] {exc.code} {exc.message} | path={request.url.path}"
    )
    return _error_response(request, exc.http_status, exc.code, exc.message, exc.data)


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    logger.warning(
        f"[HTTPException] status={exc.status_code} detail={exc.detail} | path={request.url.path}"
    )
    return _error_response(request, exc.status_code, exc.status_code * 100, str(exc.detail))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    logger.warning(
        f"[ValidationError] {len(errors)} 个字段校验失败 | path={request.url.path} | errors={errors}"
    )
    # 整理字段错误信息
    field_errors = [
        {"field": ".".join(str(loc) for loc in e["loc"]), "msg": e["msg"]}
        for e in errors
    ]
    return _error_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        42200,
        "请求参数校验失败",
        field_errors,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"[UnhandledException] {type(exc).__name__}: {exc} | path={request.url.path}\n"
        + traceback.format_exc()
    )
    return _error_response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        50000,
        "服务器内部错误，请稍后重试",
    )


# --------------------------------------------------------------------------- #
# 注册到 FastAPI
# --------------------------------------------------------------------------- #
def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
