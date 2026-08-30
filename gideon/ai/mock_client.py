from typing import Any

from gideon.ai.client import AIClient
from gideon.ai.tool_call import ToolCall


class MockAIClient(AIClient):
    """
    Тестовый AI-клиент.
    """

    def chat(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
    ) -> str | ToolCall:

        if not messages:
            return "No messages received."

        last_message = messages[-1]
        text = last_message.get("content", "")

        if text == "test_tool":
            return ToolCall(
                tool_name="test",
                arguments={
                    "message": "Hello from Mock AI"
                },
            )

        return f"Mock AI received: {text}"