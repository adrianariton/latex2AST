from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
import z3


class Symbol(MathNode):
    def __init__(self, name):
        self.name = name
        self.fname = "symbol"

    def to_latex(self):
        return self.name

    def to_wolfram(self):
        return self.name

    def to_z3(self):
        return z3.Real(self.name)

    @staticmethod
    def consume(parser: "Parser", command: str):
        return Symbol(f"\\{command}")
