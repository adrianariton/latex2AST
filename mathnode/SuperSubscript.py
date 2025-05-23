from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
from mathnode.Symbol import Symbol
from mathnode.Constant import Constant
import z3


class Superscript(MathNode):
    def __init__(self, base: MathNode, exponent: MathNode):
        self.base = base
        self.exponent = exponent
        self.fname = "superscript"

    def to_wolfram(self):
        return f"Power[{self.base.to_wolfram()}, {self.exponent.to_wolfram()}]"

    def to_latex(self):
        return f"{self.base.to_latex()}^{{{self.exponent.to_latex()}}}"

    def to_z3(self):
        return self.base.to_z3() ** self.exponent.to_z3()


class Subscript(MathNode):
    def __init__(self, base, subscript):
        self.base = base
        self.subscript = subscript
        self.fname = "subscript"

    def to_wolfram(self):
        return f"Subscript[{self.base.to_wolfram()}, {self.subscript.to_wolfram()}]"

    def to_latex(self):
        return f"sub({self.base.to_latex()}_{{{self.subscript.to_latex()}}})"

    def to_z3(self):
        def _get(b):
            if isinstance(b, Symbol):
                return b.name
            if isinstance(b, Constant):
                return str(b.value)
            return None

        if isinstance(self.base, Symbol) and (
            isinstance(self.subscript, Symbol) or isinstance(self.subscript, Constant)
        ):
            return z3.Real(self.base.name + "_" + _get(self.subscript))
        else:
            raise Exception("Invalid operands for Z3 Subscript")
