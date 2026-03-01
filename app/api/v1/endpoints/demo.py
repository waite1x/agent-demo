"""
演示端点：展示正常响应、业务异常、分页等典型用法
"""
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.schemas.response import ApiResponse, PageResponse
from app.core.exceptions import NotFoundError, AppException

logger = logging.getLogger(__name__)
router = APIRouter()

# 模拟数据
_FAKE_ITEMS = [{"id": i, "name": f"item-{i}", "value": i * 10} for i in range(1, 21)]


class CreateItemRequest(BaseModel):
    """创建资源请求体"""
    name: str = Field(..., description="资源名称，不能为空", example="my-item")


@router.get(
    "",
    summary="获取列表（分页）",
    description="支持分页和关键字过滤的资源列表接口。",
    response_model=ApiResponse,
)
async def list_items(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    keyword: Optional[str] = Query(None, description="关键字过滤"),
):
    logger.info(f"list_items | page={page} page_size={page_size} keyword={keyword}")
    items = _FAKE_ITEMS
    if keyword:
        items = [i for i in items if keyword.lower() in i["name"].lower()]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]

    return ApiResponse.ok(
        data=PageResponse(
            items=page_items,
            total=total,
            page=page,
            page_size=page_size,
        ).model_dump()
    )


@router.get(
    "/{item_id}",
    summary="获取单个资源",
    description="通过 `item_id` 获取具体资源，不存在时返回 404。",
    response_model=ApiResponse,
    responses={404: {"description": "资源不存在"}},
)
async def get_item(item_id: int):
    logger.info(f"get_item | item_id={item_id}")
    item = next((i for i in _FAKE_ITEMS if i["id"] == item_id), None)
    if not item:
        raise NotFoundError(message=f"资源 id={item_id} 不存在")
    return ApiResponse.ok(data=item)


@router.post(
    "",
    summary="创建资源（演示参数校验）",
    description="创建新资源，`name` 字段不能为空，否则返回业务异常。",
    response_model=ApiResponse,
    status_code=200,
)
async def create_item(payload: CreateItemRequest):
    logger.info(f"create_item | payload={payload}")
    name = payload.name.strip()
    if not name:
        raise AppException(code=40001, message="name 字段不能为空")
    new_item = {"id": len(_FAKE_ITEMS) + 1, "name": name, "value": 0}
    _FAKE_ITEMS.append(new_item)
    return ApiResponse.ok(data=new_item, message="创建成功")
