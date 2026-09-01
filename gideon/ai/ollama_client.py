from typing import Any

from ollama import Client

from gideon.ai.client import AIClient
from gideon.ai.tool_call import ToolCall


class OllamaClient(AIClient):
    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
    ):
        self._model = model
        self._client = Client(host=host)

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> str | ToolCall:
        response = self._client.chat(
            model=self._model,
            messages=messages,
            tools=tools or [],
        )

        message = response["message"]

        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]

            return ToolCall(
                tool_name=tool_call["function"]["name"],
                arguments=tool_call["function"]["arguments"],
            )

        return message.get("content", "")