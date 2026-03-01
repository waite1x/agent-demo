"""
自定义路由类：自动从函数 docstring 提取 summary 与 description。

规则：
  - 第一行非空文本 → summary
  - 其余内容       → description（保留 Markdown 格式）
"""
import inspect
from enum import Enum
from typing import Any, Callable, List, Optional, Type, Union

from fastapi import APIRouter
from fastapi.routing import APIRoute


class DocstringRoute(APIRoute):
    """读取 endpoint 函数的 docstring，自动填充 summary / description。"""

    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        doc = inspect.getdoc(endpoint)  # 已去除公共缩进
        if doc:
            lines = doc.splitlines()
            # 第一行作为 summary（仅在未显式传入时覆盖）
            if not kwargs.get("summary"):
                kwargs["summary"] = lines[0].strip()
            # 剩余非空内容作为 description
            if not kwargs.get("description"):
                rest = "\n".join(lines[1:]).strip()
                if rest:
                    kwargs["description"] = rest

        super().__init__(path, endpoint, **kwargs)


class AppAPIRouter(APIRouter):
    """预绑定 DocstringRoute 的 APIRouter，无需手动传 route_class。"""

    def __init__(
        self,
        *,
        tags: Optional[List[Union[str, Enum]]] = None,
        route_class: Type[APIRoute] = DocstringRoute,
        **kwargs: Any,
    ) -> None:
        super().__init__(tags=tags, route_class=route_class, **kwargs)
