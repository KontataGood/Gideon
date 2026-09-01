from abc import ABC, abstractmethod


class Platform(ABC):
    """
    Базовый интерфейс платформенных возможностей Gideon.
    """

    @abstractmethod
    def open_application(self, name: str) -> bool:
        """Открывает приложение."""
        raise NotImplementedError

    @abstractmethod
    def is_process_running(self, name: str) -> bool:
        """Проверяет наличие процесса."""
        raise NotImplementedError

    @abstractmethod
    def stop_process(self, name: str) -> bool:
        """Останавливает процесс."""
        raise NotImplementedError