from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode


class BinaryOperator(MathNode):

    LaTeX_OP_to_WOLFRAM_Function = {
        "&": "And",
        "|": "Or",
        "and": "And",
        "or": "Or",
        "+": "Plus",
        "*": "Times",
        "times": "Times",
        "^": "Power",
        "-": "_Minus",
        "/": "_Divide",
        "div": "_Divide",
        "=": "Equals",
        "approx": "Equals",  # TODO: check
        "<": "Less",
        "lt": "Less",
        "le": "LessOrEqual",
        "leq": "LessOrEqual",
        ">": "Greater",
        "to": "To",
        "gt": "Greater",
        "ge": "GreaterOrEqual",
        "geq": "GreaterOrEqual",
        "subset": "Subset",  # TODO: check
        "supset": "Supset",  # TODO: check
        "subseteq": "Subseteq",  # TODO: check
        "supseteq": "Supseteq",  # TODO: check
    }
    OPERATORS = [
        ["&", "|", "or", "and", ","],
        [
            "=",
            "to",
            "eq",
            "ge",
            "geq",
            "le",
            "leq",
            "lt",
            "gt",
            ">",
            "<",
            "subset",
            "supset",
            "subseteq",
            "supseteq",
            "approx",
        ],
        ["+", "-"],
        ["*", "/", "times", "div", "otimes", "oplus", "cup", "cap"],
        ["^"],
    ]

    def __init__(self, operator, left: MathNode, right: MathNode):
        self.operator = operator
        self.left = left
        self.right = right
        self.fname = operator

    @staticmethod
    def get_eq_ops():
        return BinaryOperator.OPERATORS[1]

    def to_z3(self):
        if self.operator == "+":
            return self.left.to_z3() + self.right.to_z3()
        elif self.operator == "-":
            return self.left.to_z3() - self.right.to_z3()
        elif self.operator == "*":
            return self.left.to_z3() * self.right.to_z3()
        elif self.operator == "times":
            return self.left.to_z3() * self.right.to_z3()
        elif self.operator == "/":
            return self.left.to_z3() / self.right.to_z3()
        elif self.operator == "^":
            return self.left.to_z3() ** self.right.to_z3()
        elif self.operator == "=" or self.operator == "eq" or self.operator == "approx":
            return self.left.to_z3() == self.right.to_z3()
        elif self.operator == ">" or self.operator == "gt":
            return self.left.to_z3() > self.right.to_z3()
        elif self.operator == "<" or self.operator == "lt":
            return self.left.to_z3() < self.right.to_z3()
        elif self.operator == "ge" or self.operator == "geq":
            return self.left.to_z3() >= self.right.to_z3()
        elif self.operator == "le" or self.operator == "leq":
            return self.left.to_z3() >= self.right.to_z3()
        else:
            raise Exception(f"{self.operator} has no equivalent in z3")

    def to_latex(self):
        left_latex = self.left.to_latex()
        right_latex = self.right.to_latex()
        op = self.operator if self.operator.startswith("\\") else self.operator
        return f"({left_latex} {op} {right_latex})"

    def to_wolfram(self):
        left_wolfram = self.left.to_wolfram()
        right_wolfram = self.right.to_wolfram()
        op = self.operator if self.operator.startswith("\\") else self.operator
        wop = BinaryOperator.LaTeX_OP_to_WOLFRAM_Function.get(op, None)
        if wop is None:
            raise Exception(f"Operation {wop} unimplemented for wolfram")

        if wop == "_Minus":
            return f"Plus[{left_wolfram}, Times[-1, {right_wolfram}]]"
        if wop == "_Divide":
            return f"Times[{left_wolfram}, Inv[{right_wolfram}]]"
        return f"{wop}[{left_wolfram}, {right_wolfram}]"

    @staticmethod
    def all_operators():
        return sum(BinaryOperator.OPERATORS, start=[])

    @staticmethod
    def is_operator(cmd: str):
        return (cmd in BinaryOperator.all_operators()) or (
            f"\\{cmd}" in BinaryOperator.all_operators()
        )
