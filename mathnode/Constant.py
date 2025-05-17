from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Constant(MathNode):
    def __init__(self, value):
        self.value = value
        self.fname = "const"

    def to_latex(self):
        return str(self.value)

    def to_wolfram(self):
        return str(self.value)

    @staticmethod
    def consume(parser: "Parser", command: str):
        return Constant(f"\\{command}")
