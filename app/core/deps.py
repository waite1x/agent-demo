"""
FastAPI 公共依赖
"""
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import UnauthorizedError
from app.core.security import TokenError, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """解析 Bearer Token，返回完整 payload；无效则抛出 401。"""
    try:
        return decode_access_token(token)
    except TokenError as e:
        raise UnauthorizedError(message=e.message)
