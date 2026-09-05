from typing import Any

from gideon.platforms.base import Platform
from gideon.tools.base import Tool


class OpenApplicationTool(Tool):

    def __init__(self, platform: Platform):
        self._platform = platform

    @property
    def name(self) -> str:
        return "open_application"

    @property
    def description(self) -> str:
        return "Opens an application on the user's computer."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": (
                        "Name or path of the application to open."
                    ),
                }
            },
            "required": ["application"],
        }

    def execute(self, **kwargs: Any) -> str:
        application = kwargs["application"]

        self._platform.open_application(application)

        return f"Opened application: {application}"
