from typing import Any

from openai import OpenAI

from gideon.ai.client import AIClient
from gideon.ai.tool_call import ToolCall


class OpenAIClient(AIClient):
    """
    Клиент OpenAI для Gideon.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> str | ToolCall:

        response = self._client.responses.create(
            model=self._model,
            input=messages,
            tools=self._build_tools(tools),
        )

        for item in response.output:
            if item.type == "function_call":
                return ToolCall(
                    tool_name=item.name,
                    arguments=self._parse_arguments(
                        item.arguments
                    ),
                )

        return response.output_text

    @staticmethod
    def _build_tools(
        tools: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:

        if not tools:
            return []

        return [
            {
                "type": "function",
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
            for tool in tools
        ]

    @staticmethod
    def _parse_arguments(
        arguments: str,
    ) -> dict[str, Any]:

        import json

        return json.loads(arguments)