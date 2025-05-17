from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
from mathnode.Constant import Constant
import re


class Diff(MathNode):
    example_message = r"\diff{f}{x} | \diff{f}{x}{x=2} | \diff*[4]{f}{x} | \diff*[4]{f}{x}{x=2}"

    def __init__(self, expresion, variable, set_expression=None, times=1):
        self.expresion = expresion
        self.variable = variable
        self.times = times
        self.set_expression = set_expression
        self.fname = "diff"

    def to_latex(self):
        if self.set_expression is None:
            return f"\\diff*[{self.times.to_latex()}]{{{self.expresion.to_latex()}}}{{{self.variable.to_latex()}}}"
        else:
            return f"\\diff*[{self.times.to_latex()}]{{{self.expresion.to_latex()}}}{{{self.variable.to_latex()}}}{{{self.set_expression.to_latex()}}}"

    def to_wolfram(self):
        return f"Derivative[{self.times.to_wolfram()}][{self.expresion.to_wolfram()}][{self.variable.to_wolfram()}] /. [{self.set_expression.to_wolfram()}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        times = Constant(1)
        if parser.current_token()[1] == "*":
            parser.consume_token()
            parser.expect_current("[", f"Example differentiation: {Diff.example_message}")
            times = parser.parse_argument("[]")
        expression = parser.parse_argument()
        diff_var = parser.parse_argument()
        set_var = None
        if parser.current_token()[1] == "{":  # we have set interval
            set_var = parser.parse_argument()
        return Diff(expression, diff_var, set_expression=set_var, times=times)
