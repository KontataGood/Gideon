import ast
import operator

from gideon.tools.base import Tool


class CalculatorTool(Tool):

    name = "calculator"

    description = (
        "Calculates a mathematical expression."
    )

    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to calculate.",
            }
        },
        "required": ["expression"],
    }

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def execute(self, expression: str):
        tree = ast.parse(
            expression,
            mode="eval",
        )

        return self._evaluate(tree.body)

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError(
                "Only numbers are allowed."
            )

        if isinstance(node, ast.BinOp):
            operation = self._operators.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported operator."
                )

            return operation(
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operation = self._operators.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported operator."
                )

            return operation(
                self._evaluate(node.operand)
            )

        raise ValueError(
            "Unsupported expression."
        )