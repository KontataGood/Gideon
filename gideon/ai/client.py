from abc import ABC, abstractmethod
from typing import Any

from gideon.ai.tool_call import ToolCall


class AIClient(ABC):

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> str | ToolCall:
        raise NotImplementedError