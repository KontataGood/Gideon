from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Базовый интерфейс инструмента Gideon.

    Этот интерфейс считается частью API Gideon.
    """

    API_VERSION = 1

    @property
    @abstractmethod
    def name(self) -> str:
        """Уникальное имя инструмента."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Описание инструмента для AI."""
        raise NotImplementedError

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """JSON Schema параметров инструмента."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Выполняет инструмент."""
        raise NotImplementedError