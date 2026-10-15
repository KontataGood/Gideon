from unittest.mock import Mock

import pytest

from gideon.core.event_type import EventType
from gideon.tools.base import Tool
from gideon.tools.executor import ToolExecutor
from gideon.tools.registry import ToolRegistry


class DummyTool(Tool):
    @property
    def name(self) -> str:
        return "dummy"

    @property
    def description(self) -> str:
        return "A tool for testing."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
            "required": ["message"],
            "additionalProperties": False,
        }

    def execute(self, **kwargs):
        return f"Result: {kwargs['message']}"


class FailingTool(DummyTool):
    @property
    def name(self) -> str:
        return "failing"

    def execute(self, **kwargs):
        raise RuntimeError("Test failure")


@pytest.fixture
def setup_executor():
    registry = ToolRegistry()
    event_bus = Mock()

    registry.register(DummyTool())

    executor = ToolExecutor(
        registry=registry,
        event_bus=event_bus,
    )

    return executor, event_bus, registry


def test_execute_returns_result(setup_executor):
    executor, event_bus, _ = setup_executor

    result = executor.execute("dummy", message="Hello")

    assert result == "Result: Hello"
    assert event_bus.publish.call_count == 2


def test_execute_publishes_started_and_finished(setup_executor):
    executor, event_bus, _ = setup_executor

    executor.execute("dummy", message="Hello")

    events = [
        call.args[0].type
        for call in event_bus.publish.call_args_list
    ]

    assert events == [
        EventType.TOOL_STARTED,
        EventType.TOOL_FINISHED,
    ]


def test_unknown_tool_raises_error(setup_executor):
    executor, event_bus, _ = setup_executor

    with pytest.raises(ValueError, match="not registered"):
        executor.execute("unknown")

    event_bus.publish.assert_not_called()


def test_failed_tool_publishes_failed_event(setup_executor):
    executor, event_bus, registry = setup_executor
    registry.register(FailingTool())

    with pytest.raises(RuntimeError, match="Test failure"):
        executor.execute("failing", message="Hello")

    events = [
        call.args[0].type
        for call in event_bus.publish.call_args_list
    ]

    assert events == [
        EventType.TOOL_STARTED,
        EventType.TOOL_FAILED,
    ]