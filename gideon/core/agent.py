from gideon.ai.tool_call import ToolCall
from gideon.ai.context import ContextManager
from gideon.core.request_router import (
    RequestRouter,
    RequestType,
)


class Agent:

    def __init__(
        self,
        ai,
        tool_registry,
        tool_executor,
        context: ContextManager,
        router: RequestRouter,
    ):
        self._ai = ai
        self._tool_registry = tool_registry
        self._tool_executor = tool_executor
        self._context = context
        self._router = router

    def process(self, text: str) -> str:
        self._context.add_user_message(text)

        route = self._router.route(text)

        if route.type == RequestType.TOOL:
            return self._execute_routed_tool(route)

        return self._process_ai_request()

    def _execute_routed_tool(self, route) -> str:
        """
        Выполняет инструмент, выбранный Router-ом,
        без обращения к AI.
        """

        if route.tool_name is None:
            raise RuntimeError(
                "Router returned TOOL without tool name."
            )

        arguments = route.arguments or {}

        result = self._tool_executor.execute(
            route.tool_name,
            **arguments,
        )

        self._context.add_tool_result(
            route.tool_name,
            result,
        )

        return str(result)

    def _process_ai_request(self) -> str:
        """
        Обрабатывает запрос через AI.
        """

        max_tool_calls = 5

        for _ in range(max_tool_calls):

            response = self._ai.chat(
                messages=self._context.get_messages(),
                tools=self._tool_registry.get_schemas(),
                think=True,
            )

            if not isinstance(response, ToolCall):

                self._context.add_assistant_message(
                    response
                )

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