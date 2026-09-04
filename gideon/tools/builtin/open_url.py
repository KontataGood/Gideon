from gideon.platforms.base import Platform
from gideon.tools.base import Tool


class OpenUrlTool(Tool):

    name = "open_url"

    description = (
        "Opens a URL in the default web browser."
    )

    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL to open.",
            }
        },
        "required": ["url"],
    }

    def __init__(self, platform: Platform):
        self._platform = platform

    def execute(self, url: str) -> str:
        self._platform.open_url(url)

        return f"Opened URL: {url}"