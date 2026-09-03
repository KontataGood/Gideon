import platform as system_platform

from gideon.platforms.base import Platform
from gideon.platforms.macos.platform import MacOSPlatform
from gideon.platforms.windows.platform import WindowsPlatform


class PlatformFactory:
    """
    Создаёт реализацию Platform для текущей ОС.
    """

    @staticmethod
    def create() -> Platform:
        current_os = system_platform.system()

        if current_os == "Windows":
            return WindowsPlatform()

        if current_os == "Darwin":
            return MacOSPlatform()

        raise RuntimeError(
            f"Unsupported operating system: {current_os}"
        )