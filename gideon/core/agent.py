from gideon.ai.tool_call import ToolCall
from gideon.ai.context import ContextManager


class Agent:

    MAX_TOOL_CALLS = 5

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

        max_tool_calls = 5

        for _ in range(max_tool_calls):

            tools = self._tool_registry.get_schemas()

            response = self._ai.chat(
                messages=self._context.get_messages(),
                tools=tools,
            )

            if not isinstance(response, ToolCall):
                self._context.add_assistant_message(response)

                return response

            self._context.add_tool_call(
                response.tool_name,
                response.arguments,
            )

            result = self._tool_executor.execute(
                response.tool_name,
                **response.arguments,
            )

            self._context.add_tool_result(
                response.tool_name,
                result,
            )

        raise RuntimeError(
            "Maximum number of tool calls exceeded."
        )