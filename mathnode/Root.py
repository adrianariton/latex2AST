from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Root(MathNode):
    example_message = r"\sqrt[4]{4*x} | \sqrt{4*x}"

    def __init__(self, degree, radicand):
        self.degree = degree  # None for square root
        self.radicand = radicand
        self.fname = "sqrt"

    def to_latex(self):
        if self.degree is None:
            return f"\\sqrt{{{self.radicand.to_latex()}}}"
        else:
            return f"\\sqrt[{self.degree.to_latex()}]{{{self.radicand.to_latex()}}}"

    def to_wolfram(self):
        return f"Pow[{self.radicand.to_wolfram()}, Inv[{self.degree.to_wolfram()}]]"

    @staticmethod
    def consume(parser: "Parser", command: str):
        if parser.current_token()[1] == "[":
            degree = parser.parse_argument(separator="[]")
            radicand = parser.parse_argument()
            return Root(degree, radicand)
        else:
            radicand = parser.parse_argument()
            return Root(None, radicand)
