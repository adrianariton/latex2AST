from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
from mathnode.Constant import Constant


class Log(MathNode):
    example_message = r"\log_{a} b | \log_a {b} | \log_a^c {b}"

    def __init__(self, base, expression, exponent):
        self.base = base
        self.expression = expression
        self.exponent = exponent
        self.fname = "log"

    def to_latex(self):
        return f"\\log_{{{self.base.to_latex()}}}^{{{self.exponent.to_latex()}}} {{{self.expression.to_latex()}}}"

    def to_wolfram(self):
        return f"Log[{self.base.to_wolfram()}, {self.exponent.to_wolfram()}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        base = Constant(10)
        exponent = Constant(1)
        if parser.current_token()[1] == "_":
            parser.consume_token()
            base = parser.parse_argument("Any")
            if parser.current_token()[1] == "^":
                parser.consume_token()
                exponent = parser.parse_argument("Any")
        expression = parser.parse_argument("Any")
        return Log(base, expression, exponent)
