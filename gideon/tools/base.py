from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Базовый интерфейс инструмента Gideon.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Уникальное имя инструмента."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Описание инструмента."""
        raise NotImplementedError

    @property
    def parameters(self) -> dict[str, Any]:
        """
        Описание параметров инструмента.

        Формат предназначен для передачи AI.
        """

        return {}

    def schema(self) -> dict[str, Any]:
        """
        Возвращает полную схему инструмента.
        """

        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Выполняет инструмент."""
        raise NotImplementedError