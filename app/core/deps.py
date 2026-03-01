"""
FastAPI 公共依赖
"""
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import UnauthorizedError
from app.core.security import TokenError, decode_access_token

_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    """从 Authorization: Bearer <token> 头中提取并验证 JWT，返回完整 payload；无效则抛出 401。"""
    try:
        return decode_access_token(credentials.credentials)
    except TokenError as e:
        raise UnauthorizedError(message=e.message)
