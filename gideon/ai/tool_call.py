from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    """
    Запрос AI на выполнение инструмента.
    """

    tool_name: str
    arguments: dict[str, Any]