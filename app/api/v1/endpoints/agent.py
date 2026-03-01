"""
Agent 端点：AI Agent 工作流触发接口
"""
import logging
from typing import Any, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.calculator.workflow import calc_workflow
from app.schemas.response import ApiResponse

logger = logging.getLogger(__name__)
router = APIRouter()


# --------------------------------------------------------------------------- #
# 请求 / 响应 Schema
# --------------------------------------------------------------------------- #
class CalcRequest(BaseModel):
    """计算器 Agent 请求体"""
    numbers: Optional[List[int]] = Field(
        default=None,
        description="待计算的整数列表（留空则自动生成 10 个 1-100 的随机数）",
        example=[10, 20, 30, 40, 50],
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

    numbers = body.numbers or [random.randint(1, 100) for _ in range(10)]
    logger.info(f"agent_calculator | numbers={numbers}")
    event = await calc_workflow.run(",".join(str(n) for n in numbers))
    return ApiResponse.ok(data=event.get_outputs())
