from abc import ABC, abstractmethod


class Platform(ABC):
    """
    Базовый интерфейс платформы Gideon.
    """

    @abstractmethod
    def open_application(self, application: str) -> None:
        """Открывает приложение."""
        raise NotImplementedError

    @abstractmethod
    def is_process_running(self, process: str) -> bool:
        """Проверяет, запущен ли процесс."""
        raise NotImplementedError

    @abstractmethod
    def stop_process(self, process: str) -> None:
        """Останавливает процесс."""
        raise NotImplementedError

    @abstractmethod
    def open_url(self, url: str) -> None:
        """Открывает URL в браузере."""
        raise NotImplementedError