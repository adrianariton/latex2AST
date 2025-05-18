from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
import z3


class Apply(MathNode):
    def __init__(self, function: MathNode, argument: MathNode):
        self.function = function
        self.argument = argument
        self.fname = "apply"

    def to_latex(self):
        return f"\\{self.function.to_latex()}{{{self.argument.to_latex()}}}"

    def to_wolfram(self):
        return f"Construct[{self.function.to_wolfram()}, {self.argument.to_wolfram()}]"

    def to_z3(self):
        return self.function.to_z3() * self.argument.to_z3()

    @staticmethod
    def consume(parser: "Parser", command: str):
        pass
