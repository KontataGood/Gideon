from unittest.mock import Mock

import pytest

from gideon.tools.registry import ToolRegistry


def make_tool(name: str):
    tool = Mock()
    tool.name = name
    tool.schema.return_value = {
        "type": "function",
        "function": {
            "name": name,
            "description": "Test tool",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    }
    return tool


def test_register_and_get_tool():
    registry = ToolRegistry()
    tool = make_tool("example")

    registry.register(tool)

    assert registry.get("example") is tool
    assert registry.has("example") is True


def test_get_unknown_tool():
    registry = ToolRegistry()

    assert registry.get("unknown") is None
    assert registry.has("unknown") is False


def test_duplicate_registration_raises_error():
    registry = ToolRegistry()
    registry.register(make_tool("example"))

    with pytest.raises(ValueError, match="already registered"):
        registry.register(make_tool("example"))


def test_get_all_returns_registered_tools():
    registry = ToolRegistry()
    first = make_tool("first")
    second = make_tool("second")

    registry.register(first)
    registry.register(second)

    assert registry.get_all() == [first, second]


def test_get_schemas():
    registry = ToolRegistry()
    tool = make_tool("example")
    registry.register(tool)

    assert registry.get_schemas() == [tool.schema.return_value]