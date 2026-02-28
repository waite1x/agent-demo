"""
演示端点：展示正常响应、业务异常、分页等典型用法
"""
import logging

from fastapi import APIRouter

from app.agent.calculator import calc_workflow
from app.schemas.response import ApiResponse, PageResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("cal", summary="agent calculator")
async def agent_calculator

