import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """
    Управляет конфигурацией Gideon.
    """

    def __init__(self, path: str | Path):
        self._path = Path(path)
        self._data: dict[str, Any] = {}

        self.load()

    def load(self):
        """Загружает конфигурацию из JSON."""

        if not self._path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self._path}"
            )

        with self._path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self._data = json.load(file)

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Получает значение по пути.

        Например:

            config.get("ai.model")
        """

        value: Any = self._data

        for part in key.split("."):
            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value

    def set(
        self,
        key: str,
        value: Any,
    ):
        """Изменяет значение в памяти."""

        parts = key.split(".")
        current = self._data

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current[parts[-1]] = value

    def save(self):
        """Сохраняет текущую конфигурацию."""

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self._data,
                file,
                indent=4,
                ensure_ascii=False,
            )