from gideon.tools.base import Tool


class TestTool(Tool):

    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Test tool for Gideon."

    @property
    def parameters(self) -> dict:
        return {
            "message": {
                "type": "string",
                "required": True,
                "description": "Message to return.",
            }
        }

    def execute(self, **kwargs):
        message = kwargs.get("message")

        return f"Test tool executed: {message}"