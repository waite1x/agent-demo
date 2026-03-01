"""
JWT 工具：Token 验证与解码
"""
from typing import Any, Optional

from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings


class TokenError(Exception):
    """Token 验证失败"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def decode_access_token(token: str) -> dict[str, Any]:
    """解码并验证 Token，返回完整 payload。

    Raises:
        TokenError: Token 已过期或签名无效时抛出。
    """
    try:
        return jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise TokenError("Token 已过期")
    except JWTError:
        raise TokenError("Token 无效")
