from typing import List, Any

from agent_framework import AgentResponse

from app.schemas import ResponseBase


class WorkflowResponse(ResponseBase):
    author_name: str | None = None
    text: str | None = None


def parse_workflow_response(response: List[Any]) -> List[WorkflowResponse]:
    """
    解析 Agent 输出的 JSON 字符串，提取 result 字段。
    处理可能的格式错误或缺失字段，返回统一结构的字典。
    """
    results = []
    if not response:
        return []

    for item in response:
        if isinstance(item, AgentResponse):
            for message in item.messages:
                results.append(WorkflowResponse(author_name=message.author_name, text=message.text))

    return results
