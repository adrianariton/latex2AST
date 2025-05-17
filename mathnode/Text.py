from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class Text(MathNode):
    def __init__(self, value):
        self.value = value
        self.fname = "text"

    def to_latex(self):
        return str(self.value)

    def to_wolfram(self):
        return str(self.value)

    @staticmethod
    def consume(parser: "Parser", command: str):
        parser.expect_current("{")
        parser.consume_token()
        var_name = ""
        while parser.current_token()[1] != "}":
            c = parser.current_token()[1]
            var_name += c
            parser.consume_token()
        parser.consume_token()
        return Text(value=var_name)
