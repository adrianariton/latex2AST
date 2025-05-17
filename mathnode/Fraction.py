from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Fraction(MathNode):
    example_message = r"\frac{2}{3}"

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.fname = "frac"

    def to_latex(self):
        return f"\\frac{{{self.numerator.to_latex()}}}{{{self.denominator.to_latex()}}}"

    def to_wolfram(self):
        return f"Multiply[{self.numerator.to_wolfram()}, Inv[{self.denominator.to_wolfram()}]]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        numerator = parser.parse_argument()
        denominator = parser.parse_argument()
        return Fraction(numerator, denominator)
