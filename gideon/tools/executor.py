from typing import Any

from gideon.core.event import Event
from gideon.core.event_type import EventType
from gideon.tools.registry import ToolRegistry


class ToolExecutor:
    """
    Выполняет инструменты через ToolRegistry.
    """

    def __init__(self, registry: ToolRegistry, event_bus):
        self._registry = registry
        self._event_bus = event_bus

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Выполняет инструмент по имени.
        """

        tool = self._registry.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        self._event_bus.publish(
            Event(
                type=EventType.TOOL_STARTED,
                data={
                    "tool": tool_name,
                    "arguments": kwargs,
                },
            )
        )

        try:
            result = tool.execute(**kwargs)

        except Exception as error:
            self._event_bus.publish(
                Event(
                    type=EventType.TOOL_FAILED,
                    data={
                        "tool": tool_name,
                        "error": str(error),
                    },
                )
            )

            raise

        self._event_bus.publish(
            Event(
                type=EventType.TOOL_FINISHED,
                data={
                    "tool": tool_name,
                    "result": result,
                },
            )
        )

        return result