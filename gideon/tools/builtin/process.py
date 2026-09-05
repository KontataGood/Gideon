from typing import Any

from gideon.platforms.base import Platform
from gideon.tools.base import Tool


class ProcessTool(Tool):

    def __init__(self, platform: Platform):
        self._platform = platform

    @property
    def name(self) -> str:
        return "process"

    @property
    def description(self) -> str:
        return (
            "Checks whether a process is running or stops a running process."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["check", "stop"],
                    "description": (
                        "Action to perform: check or stop."
                    ),
                },
                "process": {
                    "type": "string",
                    "description": (
                        "Process name, for example Steam.exe."
                    ),
                },
            },
            "required": ["action", "process"],
        }

    def execute(self, **kwargs: Any) -> str:
        action = kwargs["action"]
        process = kwargs["process"]

        if action == "check":
            running = self._platform.is_process_running(process)

            if running:
                return f"Process is running: {process}"

            return f"Process is not running: {process}"

        if action == "stop":
            self._platform.stop_process(process)

            return f"Stopped process: {process}"

        raise ValueError(
            f"Unsupported process action: {action}"
        )
