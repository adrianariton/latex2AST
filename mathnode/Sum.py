from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
from mathnode.BinaryOperator import BinaryOperator


class Sum(MathNode):
    # \int_{a}^{b} x^2 dx
    example_message = r"\sum_{i=0}^{7} C_i"

    def __init__(self, expresion, variable, interval=None):
        self.interval = interval
        self.variable = variable
        self.expresion = expresion
        self.fname = "sum"

    def to_latex(self):
        if self.interval is None:
            return f"\\sum{{{self.expresion.to_latex()}}}"
        else:
            return f"\\sum_{{{self.interval[0].to_latex()}}}^{{{self.interval[1].to_latex()}}} {{{self.expresion.to_latex()}}}"

    def to_wolfram(self):
        return f"Sum[{self.expresion.to_wolfram()}, {'{'} {self.variable.to_wolfram()}, {self.interval[0].to_wolfram()}, {self.interval[1].to_wolfram()} {'}'}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        if parser.current_token()[1] == "_":
            parser.consume_token()
            int_min = parser.parse_argument("Any")
            parser.expect_current(
                "^",
                message="Cannot specify just lower bound for the integral. Example: "
                + Sum.example_message,
            )
            parser.consume_token()
            int_max = parser.parse_argument("Any")
            expr = parser.parse_argument(separator="Any")
            assert (
                isinstance(int_min, BinaryOperator)
                and int_min.operator in BinaryOperator.get_eq_ops()
            ), "lolololili"
            variable = int_min.left
            return Sum(expr, variable, [int_min, int_max])
        else:
            return Sum(expr, None)
