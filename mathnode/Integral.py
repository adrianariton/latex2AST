from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Integral(MathNode):
    # \int_{a}^{b} x^2 dx
    example_message = r"\int_{a}^{b} x^2 dx | \int x^2 + 2x dx"

    def __init__(self, expresion, variable, interval=None):
        self.interval = interval
        self.variable = variable
        self.expresion = expresion
        self.fname = "int"

    def to_latex(self):
        if self.interval is None:
            return f"\\{self.fname}{{{self.expresion.to_latex()}}} d({self.variable.to_latex()})"
        else:
            return f"\\{self.fname}_{{{self.interval[0].to_latex()}}}^{{{self.interval[1].to_latex()}}} {{{self.expresion.to_latex()}}}  d({self.variable.to_latex()})"

    def to_wolfram(self):
        return f"Integral[{self.expresion.to_wolfram()}, {'{'} {self.variable.to_wolfram()}, {self.interval[0].to_wolfram()}, {self.interval[1].to_wolfram()} {'}'}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        if parser.current_token()[1] == "_":
            parser.consume_token()
            int_min = parser.parse_argument("Any")
            parser.expect_current(
                "^",
                message="Cannot specify just lower bound for the integral. Example: "
                + Integral.example_message,
            )
            parser.consume_token()
            int_max = parser.parse_argument("Any")
            expresion = parser.parse_term_until("d")
            variable = parser.parse_argument(separator="Any")
            return Integral(expresion, variable, [int_min, int_max])
        else:
            expresion = parser.parse_term_until("d")
            variable = parser.parse_argument(separator="Any")
            return Integral(expresion, variable)
