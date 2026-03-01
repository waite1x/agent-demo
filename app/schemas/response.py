"""
统一 API 响应 Schema
所有接口均返回相同的包装格式，方便前端统一处理。

成功格式：
  {
    "success": true,
    "code": 200,
    "message": "ok",
    "data": { ... }
  }

分页数据放在 data 内：
  {
    "success": true,
    "code": 200,
    "message": "ok",
    "data": {
      "items": [...],
      "total": 100,
      "page": 1,
      "pageSize": 10,
      "totalPages": 10
    }
  }
"""
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import Field

from app.schemas import ResponseBase

DataT = TypeVar("DataT")


class ApiResponse(ResponseBase, Generic[DataT]):
    """通用响应模型"""

    success: bool = True
    http_code: int = 200
    message: str = "ok"
    data: Optional[DataT] = None

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "ok",
        code: int = 200,
    ) -> "ApiResponse":
        return cls(success=True, http_code=code, message=message, data=data)

    @classmethod
    def fail(
        cls,
        message: str = "error",
        code: int = 40000,
        data: Any = None,
    ) -> "ApiResponse":
        return cls(success=False, http_code=code, message=message, data=data)


class PageResponse(ResponseBase, Generic[DataT]):
    """分页数据模型"""

    items: List[Any] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 10
    total_pages: int = 0

    def model_post_init(self, __context: Any) -> None:
        if self.page_size > 0:
            import math
            object.__setattr__(
                self,
                "total_pages",
                math.ceil(self.total / self.page_size),
            )
