from typing import Any

from gideon.ai.client import AIClient
from gideon.ai.tool_call import ToolCall


class AIManager:

    def __init__(self, client: AIClient):
        self._client = client

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        think: bool = False,
    ) -> str | ToolCall:

        return self._client.chat(
            messages=messages,
            tools=tools,
            think=think,
        )
