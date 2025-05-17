from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Function(MathNode):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument
        self.fname = "function"

    def to_latex(self):
        return f"\\{self.name}{{{self.argument.to_latex()}}}"

    def to_wolfram(self):
        return f"{self.name.title()}[{self.argument.to_wolfram()}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        arg = parser.parse_argument()
        return Function(command, arg)
