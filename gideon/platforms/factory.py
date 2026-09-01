import platform

from gideon.platforms.base import Platform
from gideon.platforms.windows.platform import WindowsPlatform
from gideon.platforms.macos.platform import MacOSPlatform


def create_platform() -> Platform:
    """
    Создаёт реализацию платформы
    для текущей операционной системы.
    """

    system = platform.system()

    if system == "Windows":
        return WindowsPlatform()

    if system == "Darwin":
        return MacOSPlatform()

    raise RuntimeError(
        f"Unsupported platform: {system}"
    )