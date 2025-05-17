from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Apply(MathNode):
    def __init__(self, function, argument):
        self.function = function
        self.argument = argument
        self.fname = "apply"

    def to_latex(self):
        return f"\\{self.function.to_latex()}{{{self.argument.to_latex()}}}"

    def to_wolfram(self):
        return f"Construct[{self.function.to_wolfram()}, {self.argument.to_wolfram()}]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        pass
