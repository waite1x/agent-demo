"""
schemas 模块
"""
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ResponseBase(BaseModel):
    """全局基类：JSON 序列化时自动使用小驼峰命名"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
