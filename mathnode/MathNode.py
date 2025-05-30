from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser


class MathNode:
    example_message = r"- no examples -"

    def __init__(self):
        self.fname = None

    def to_z3(self):
        raise NotImplementedError("to_z3: Subclasses must implement this method.")

    def to_latex(self):
        raise NotImplementedError("to_latex: Subclasses must implement this method.")

    def to_wolfram(self):
        raise NotImplementedError("to_wolfram: Subclasses must implement this method.")

    @staticmethod
    def consume(parser: "Parser", command: str):
        raise NotImplementedError("Subclasses must implement this method.")
