from typing import Any

from agent_framework.openai import OpenAIChatClient

def create_agent(**kwargs: Any):
    client = OpenAIChatClient(
        api_key="3090a55ad1d8429e9a686f644eec4605.wE7iN1iFEhH6XFy5",
        base_url="https://open.bigmodel.cn/api/paas/v4",
        model_id='GLM-4.5')
    return  client.as_agent(**kwargs)
