import os
import shutil
import subprocess
from pathlib import Path

from gideon.platforms.base import Platform


class WindowsPlatform(Platform):
    """
    Реализация платформы Gideon для Windows.
    """

    def open_application(self, application: str) -> None:
        application = application.strip()

        if not application:
            raise ValueError("Application name cannot be empty.")

        path = Path(application)

        if path.exists():
            os.startfile(path)
            return

        executable = shutil.which(application)

        if executable:
            subprocess.Popen([executable])
            return

        executable = self._find_start_menu_application(application)

        if executable:
            os.startfile(executable)
            return

        raise FileNotFoundError(
            f"Application '{application}' was not found."
        )


    def _find_start_menu_application(
        self,
        application: str,
    ) -> Path | None:
        """
        Ищет приложение среди зарегистрированных приложений Windows.
        """

        target = self._normalize_application_name(application)

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-StartApps | "
                "Select-Object Name, AppID | "
                "ConvertTo-Json -Compress",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None

        try:
            import json

            apps = json.loads(result.stdout)

        except json.JSONDecodeError:
            return None

        if isinstance(apps, dict):
            apps = [apps]

        for app in apps:
            name = app.get("Name", "")
            app_id = app.get("AppID", "")

            if (
                self._normalize_application_name(name)
                != target
            ):
                continue

            app_path = Path(app_id)

            if app_path.exists():
                return app_path

        return None

    @staticmethod
    def _normalize_application_name(
        application: str,
    ) -> str:
        """
        Нормализует имя приложения для сравнения.
        """

        name = Path(application).stem

        return (
            name
            .lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

    def is_process_running(self, process: str) -> bool:
        process = Path(process.strip()).name

        if not process.lower().endswith(".exe"):
            process += ".exe"

        result = subprocess.run(
            [
                "tasklist",
                "/FI",
                f"IMAGENAME eq {process}",
            ],
            capture_output=True,
            text=True,
        )

        return process.lower() in result.stdout.lower()

    def stop_process(self, process: str) -> None:
        process = Path(process.strip()).name

        if not process.lower().endswith(".exe"):
            process += ".exe"

        subprocess.run(
            [
                "taskkill",
                "/IM",
                process,
                "/F",
            ],
            capture_output=True,
            text=True,
        )

    def open_url(self, url: str) -> None:
        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                url,
            ],
            shell=True,
        )
