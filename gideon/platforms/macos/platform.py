import subprocess

from gideon.platforms.base import Platform


class MacOSPlatform(Platform):
    """
    Реализация платформы Gideon для macOS.
    """

    def open_application(self, application: str) -> None:
        application = application.strip()

        if not application:
            raise ValueError(
                "Application name cannot be empty."
            )

        subprocess.Popen(
            ["open", "-a", application]
        )

    def open_url(self, url: str) -> None:
        url = url.strip()

        if not url:
            raise ValueError(
                "URL cannot be empty."
            )

        subprocess.Popen(
            ["open", url]
        )

    def is_process_running(self, process: str) -> bool:
        process = process.strip()

        if not process:
            raise ValueError(
                "Process name cannot be empty."
            )

        result = subprocess.run(
            ["pgrep", "-x", process],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    def stop_process(self, process: str) -> None:
        process = process.strip()

        if not process:
            raise ValueError(
                "Process name cannot be empty."
            )

        subprocess.run(
            ["pkill", "-x", process],
            capture_output=True,
            text=True,
        )
