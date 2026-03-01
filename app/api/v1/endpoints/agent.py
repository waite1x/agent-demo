"""
Agent 端点：AI Agent 工作流触发接口
"""
import logging
from typing import Any, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.core.utils import parse_workflow_response, WorkflowResponse
from app.schemas.response import ApiResponse

logger = logging.getLogger(__name__)

TAG_META = {
    "name": "Agent",
    "description": "AI Agent 相关接口。\n\n"
                   "目前提供基于 `agent-framework` 的**计算器工作流**示例，"
                   "演示 Fan-Out / Fan-In 多步骤 Agent 编排模式。",
}

router = APIRouter(tags=["Agent"])


# --------------------------------------------------------------------------- #
# 请求 / 响应 Schema
# --------------------------------------------------------------------------- #
class CalcRequest(BaseModel):
    """计算器 Agent 请求体"""
    numbers: Optional[List[int] | None] = Field(
        default=None,
        description="待计算的整数列表（留空则自动生成 10 个 1-100 的随机数）",
        examples=[[10, 20, 30, 40, 50]],
    )


# --------------------------------------------------------------------------- #
# 路由
# --------------------------------------------------------------------------- #
@router.post(
    "/cal",
    summary="计算器 Agent",
    responses={
        200: {"description": "计算成功，返回 sum 与 average"},
        500: {"description": "Agent 工作流执行异常"},
    },
)
async def agent_calculator(body: CalcRequest = CalcRequest()) -> ApiResponse[List[Any]]:
    """
    触发基于 agent-framework 的计算器工作流（Fan-Out / Fan-In 模式）。

    工作流将输入数字列表分发给**求和**与**均值**两个执行器，最后汇聚为聚合结果返回。
    """
    import random
    from app.agent.calculator import workflow

    numbers = body.numbers or [random.randint(1, 100) for _ in range(10)]
    logger.info(f"agent_calculator | numbers={numbers}")
    event = await workflow.run(",".join(str(n) for n in numbers))
    outputs = [o.to_dict() if hasattr(o, "to_dict") else o for o in event.get_outputs()]
    return ApiResponse.ok(data=outputs)


class WriterRequest(BaseModel):
    """Writer Agent 请求体"""
    prompt: str = Field(..., description="写作提示语", examples=["请写一首关于春天的诗歌。"])


@router.post(
    "/writer",
    summary="Writer Agent",
    responses={
        200: {"description": "写作成功，返回生成内容"},
        500: {"description": "Agent 工作流执行异常"},
    },
)
async def agent_writer(body: WriterRequest) -> ApiResponse[List[WorkflowResponse]]:
    """
    演示基于 agent-framework 的 Writer Agent 工作流。
    """
    from app.agent.writer import workflow

    event = await workflow.run(body.prompt)
    results = event.get_outputs()
    data = parse_workflow_response(results)
    return ApiResponse.ok(data=data)
