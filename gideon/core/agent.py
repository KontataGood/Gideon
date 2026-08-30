from gideon.ai.tool_call import ToolCall
from gideon.ai.context import ContextManager


class Agent:

    def __init__(
        self,
        ai,
        tool_registry,
        tool_executor,
        context: ContextManager,
    ):
        self._ai = ai
        self._tool_registry = tool_registry
        self._tool_executor = tool_executor
        self._context = context

    def process(self, text: str) -> str:

        self._context.add_user_message(text)

        tools = self._tool_registry.get_schemas()

        response = self._ai.chat(
            messages=self._context.get_messages(),
            tools=tools,
        )

        if isinstance(response, ToolCall):

            result = self._tool_executor.execute(
                response.tool_name,
                **response.arguments,
            )

            self._context.add_tool_result(
                response.tool_name,
                result,
            )

            return str(result)

        self._context.add_assistant_message(
            response
        )

        return response