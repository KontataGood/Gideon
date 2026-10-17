import os
import shutil
import subprocess
from pathlib import Path

from gideon.platforms.base import Platform


class WindowsPlatform(Platform):
    """Реализация платформы Gideon для Windows."""

    def open_application(self, application: str) -> None:
        application = application.strip()

        if not application:
            raise ValueError("Application name cannot be empty.")

        path = Path(application).expanduser()

        # 1. Пользователь передал полный или относительный путь.
        if path.is_file():
            os.startfile(str(path.resolve()))
            return

        # 2. Приложение доступно через PATH.
        executable = shutil.which(application)

        if executable:
            subprocess.Popen([executable])
            return

        # 3. Поиск по стандартным каталогам Windows.
        executable = self._find_installed_executable(application)

        if executable is not None:
            os.startfile(str(executable))
            return

        # 4. Поиск зарегистрированных приложений в меню «Пуск».
        app_id = self._find_start_menu_application(application)

        if app_id is not None:
            subprocess.Popen(
                [
                    "explorer.exe",
                    f"shell:AppsFolder\\{app_id}",
                ]
            )
            return

        raise FileNotFoundError(
            f"Application '{application}' was not found."
        )

    def _find_installed_executable(
        self,
        application: str,
    ) -> Path | None:
        target = self._normalize_application_name(application)

        # Каталоги, в которых часто устанавливаются приложения.
        roots = [
            Path(os.environ.get("APPDATA", "")),
            Path(os.environ.get("LOCALAPPDATA", "")),
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
            Path(
                os.environ.get(
                    "ProgramFiles(x86)",
                    r"C:\Program Files (x86)",
                )
            ),
        ]

        # Сначала проверяем известные стандартные пути.
        candidates = [
            Path(os.environ.get("APPDATA", ""))
            / "Telegram Desktop"
            / "Telegram.exe",
            Path(os.environ.get("LOCALAPPDATA", ""))
            / application
            / f"{application}.exe",
        ]

        for candidate in candidates:
            if candidate.is_file():
                return candidate

        # Затем ищем совпадение по имени EXE.
        for root in roots:
            if not str(root) or not root.is_dir():
                continue

            try:
                for candidate in root.rglob("*.exe"):
                    if (
                        self._normalize_application_name(candidate.stem)
                        == target
                    ):
                        return candidate
            except (OSError, PermissionError):
                continue

        return None

    def _find_start_menu_application(
        self,
        application: str,
    ) -> str | None:
        target = self._normalize_application_name(application)

        script = (
            "Get-StartApps | "
            "Select-Object Name, AppID | "
            "ConvertTo-Json -Compress"
        )

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                script,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None

        import json

        try:
            apps = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None

        if isinstance(apps, dict):
            apps = [apps]

        for app in apps:
            name = app.get("Name", "")
            app_id = app.get("AppID", "")

            if (
                self._normalize_application_name(name) == target
                and app_id
            ):
                return app_id

        return None

    @staticmethod
    def _normalize_application_name(application: str) -> str:
        return (
            Path(application).stem
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
            ["tasklist", "/FI", f"IMAGENAME eq {process}"],
            capture_output=True,
            text=True,
            check=False,
        )

        return process.lower() in result.stdout.lower()

    def stop_process(self, process: str) -> None:
        process = Path(process.strip()).name

        if not process.lower().endswith(".exe"):
            process += ".exe"

        subprocess.run(
            ["taskkill", "/IM", process, "/F"],
            capture_output=True,
            text=True,
            check=False,
        )

    def open_url(self, url: str) -> None:
        import webbrowser

        if not webbrowser.open(url):
            raise RuntimeError(f"Could not open URL: {url}")