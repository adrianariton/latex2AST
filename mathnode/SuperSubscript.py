from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Superscript(MathNode):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
        self.fname = "superscript"

    def to_wolfram(self):
        return f"Power[{self.base.to_wolfram()}, {self.exponent.to_wolfram()}]"

    def to_latex(self):
        return f"{self.base.to_latex()}^{{{self.exponent.to_latex()}}}"


class Subscript(MathNode):
    def __init__(self, base, subscript):
        self.base = base
        self.subscript = subscript
        self.fname = "subscript"

    def to_wolfram(self):
        return f"Subscript[{self.base.to_wolfram()}, {self.subscript.to_wolfram()}]"

    def to_latex(self):
        return f"sub({self.base.to_latex()}_{{{self.subscript.to_latex()}}})"
