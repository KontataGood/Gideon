from dataclasses import dataclass
from enum import Enum


class RequestType(Enum):
    TOOL = "tool"
    AI = "ai"


@dataclass
class RouteResult:
    type: RequestType
    tool_name: str | None = None
    arguments: dict | None = None


class RequestRouter:
    """
    Определяет способ обработки запроса.

    Простые детерминированные операции выполняются напрямую
    без обращения к AI.
    """

    def route(self, text: str) -> RouteResult:
        text = text.strip()

        expression = self._extract_calculation(text)
        if expression is not None:
            return RouteResult(
                type=RequestType.TOOL,
                tool_name="calculator",
                arguments={"expression": expression},
            )

        url = self._extract_url(text)
        if url is not None:
            return RouteResult(
                type=RequestType.TOOL,
                tool_name="open_url",
                arguments={"url": url},
            )

        application = self._extract_application(text)
        if application is not None:
            return RouteResult(
                type=RequestType.TOOL,
                tool_name="open_application",
                arguments={"application": application},
            )

        return RouteResult(type=RequestType.AI)

    def _extract_calculation(self, text: str) -> str | None:
        """
        Извлекает математическое выражение
        из простого запроса пользователя.
        """

        normalized = text.lower()

        prefixes = (
            "сколько будет ",
            "посчитай ",
            "вычисли ",
            "calculate ",
        )

        for prefix in prefixes:
            if normalized.startswith(prefix):
                expression = text[len(prefix):].strip()

                if self._looks_like_expression(expression):
                    return expression

        return None

    def _extract_url(self, text: str) -> str | None:
        """
        Извлекает URL из простой команды открытия сайта.
        """

        normalized = text.lower()

        prefixes = (
            "открой ",
            "open ",
        )

        for prefix in prefixes:
            if normalized.startswith(prefix):
                url = text[len(prefix):].strip()

                if url.startswith(("http://", "https://")):
                    return url

        return None

    def _extract_application(self, text: str) -> str | None:
        """
        Извлекает название приложения
        из простой команды запуска приложения.
        """

        normalized = text.lower()

        prefixes = (
            "открой приложение ",
            "запусти приложение ",
            "open application ",
        )

        for prefix in prefixes:
            if normalized.startswith(prefix):
                application = text[len(prefix):].strip()

                if application:
                    return application

        return None

    def _looks_like_expression(self, expression: str) -> bool:
        """
        Проверяет, является ли строка математическим выражением.
        """

        allowed_characters = set("0123456789+-*/%.() ")

        return (
            bool(expression)
            and all(
                character in allowed_characters
                for character in expression
            )
            and any(character.isdigit() for character in expression)
        )