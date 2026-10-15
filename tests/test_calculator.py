import pytest

from gideon.tools.builtin.calculator import CalculatorTool


@pytest.fixture
def calculator():
    return CalculatorTool()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("6 * 7", 42),
        ("15 / 3", 5),
        ("2 ** 3", 8),
        ("10 % 3", 1),
        ("-(5 + 2)", -7),
        ("123 * 456", 56088),
        ("2 + 3 * 4", 14),
    ],
)
def test_calculate_valid_expression(calculator, expression, expected):
    assert calculator.execute(expression=expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "hello",
        "2 // 3",
        "2 < 3",
        "True",
        "2 + 'hello'",
        "[1, 2, 3]",
    ],
)
def test_reject_invalid_expression(calculator, expression):
    with pytest.raises((ValueError, TypeError, SyntaxError)):
        calculator.execute(expression=expression)


def test_division_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.execute(expression="10 / 0")