from gideon.tools.base import Tool


class ToolRegistry:
    """
    Реестр инструментов Gideon.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Регистрирует инструмент."""

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Возвращает инструмент по имени."""

        return self._tools.get(name)

    def get_all(self) -> list[Tool]:
        """Возвращает все зарегистрированные инструменты."""

        return list(self._tools.values())

    def has(self, name: str) -> bool:
        """Проверяет наличие инструмента."""

        return name in self._tools

    def get_schemas(self) -> list[dict]:
        """
        Возвращает схемы всех зарегистрированных инструментов.
        """

        return [
            tool.schema()
            for tool in self._tools.values()
        ]