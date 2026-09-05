from gideon.platforms.base import Platform
from gideon.tools.base import Tool


class OpenApplicationTool(Tool):

    name = "open_application"

    description = (
        "Opens an application on the user's computer."
    )

    parameters = {
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

    def __init__(self, platform: Platform):
        self._platform = platform

    def execute(self, application: str) -> str:
        self._platform.open_application(application)

        return f"Opened application: {application}"
