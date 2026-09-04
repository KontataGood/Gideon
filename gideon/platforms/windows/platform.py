import subprocess

from gideon.platforms.base import Platform


class WindowsPlatform(Platform):
    """
    Реализация платформы Gideon для Windows.
    """

    def open_application(self, application: str) -> None:
        subprocess.Popen(
            ["cmd", "/c", "start", "", application],
            shell=True,
        )

    def is_process_running(self, process: str) -> bool:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {process}"],
            capture_output=True,
            text=True,
        )

        return process.lower() in result.stdout.lower()

    def stop_process(self, process: str) -> None:
        subprocess.run(
            ["taskkill", "/IM", process, "/F"],
            capture_output=True,
            text=True,
        )

    def open_url(self, url: str) -> None:
        subprocess.Popen(
            ["cmd", "/c", "start", "", url],
            shell=True,
        )