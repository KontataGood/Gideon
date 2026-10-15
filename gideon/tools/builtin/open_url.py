from typing import Any

from gideon.platforms.base import Platform
from gideon.tools.base import Tool


class OpenUrlTool(Tool):
    def __init__(self, platform: Platform):
        self._platform = platform

    @property
    def name(self) -> str:
        return "open_url"

    @property
    def description(self) -> str:
        return "Opens a URL in the default web browser."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to open.",
                }
            },
            "required": ["url"],
            "additionalProperties": False,
        }

    def execute(self, **kwargs: Any) -> str:
        url = kwargs["url"]
        self._platform.open_url(url)

        return f"Opened URL: {url}"