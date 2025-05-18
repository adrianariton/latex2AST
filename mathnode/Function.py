from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
import z3


class Function(MathNode):
    def __init__(self, name, argument: MathNode):
        self.name = name
        self.argument = argument
        self.fname = "function"

    def to_z3(self):
        if self.fname == "sin":
            return z3.sin(self.argument.to_z3())
        elif self.fname == "cos":
            return z3.cos(self.argument.to_z3())
        elif self.fname == "tan":
            return z3.tan(self.argument.to_z3())
        elif self.fname == "ln":
            return z3.ln(self.argument.to_z3())
        elif self.fname == "lg":
            return z3.lg(self.argument.to_z3())

    def to_latex(self):
        return f"\\{self.name}{{{self.argument.to_latex()}}}"

    def to_wolfram(self):
        return f"{self.name.title()}[{self.argument.to_wolfram()}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        arg = parser.parse_argument()
        return Function(command, arg)
