from typing import Any


class ContextManager:
    """
    Управляет контекстом текущего диалога Gideon.
    """

    def __init__(self, system_prompt: str):
        self._messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def add_user_message(self, text: str):
        """Добавляет сообщение пользователя."""

        self._messages.append(
            {
                "role": "user",
                "content": text,
            }
        )

    def add_assistant_message(self, text: str):
        """Добавляет ответ ассистента."""

        self._messages.append(
            {
                "role": "assistant",
                "content": text,
            }
        )

    def add_tool_result(
        self,
        tool_name: str,
        result: Any,
    ):
        """Добавляет результат выполнения инструмента."""

        self._messages.append(
            {
                "role": "tool",
                "name": tool_name,
                "content": str(result),
            }
        )

    def get_messages(self) -> list[dict[str, Any]]:
        """Возвращает текущий контекст."""

        return list(self._messages)

    def clear(self):
        """Очищает историю, сохраняя system prompt."""

        system_message = self._messages[0]

        self._messages = [
            system_message
        ]