import subprocess

from gideon.platforms.base import Platform


class MacOSPlatform(Platform):
    """
    Реализация платформы Gideon для macOS.
    """

    def open_application(self, application: str) -> None:
        subprocess.Popen(
            ["open", "-a", application]
        )

    def is_process_running(self, process: str) -> bool:
        result = subprocess.run(
            ["pgrep", "-x", process],
            capture_output=True,
        )

        return result.returncode == 0

    def stop_process(self, process: str) -> None:
        subprocess.run(
            ["pkill", "-x", process],
            capture_output=True,
        )