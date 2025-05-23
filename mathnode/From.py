from mathnode import (
    Fraction,
    Root,
    Integral,
    Function,
    Constant,
    Symbol,
    MathNode,
    Diff,
    Log,
    Sum,
    CommandRule,
    Text,
)


class CommandFrom:
    def __init__(self, cmdrules: dict[MathNode]):
        self.cmdrules = cmdrules

    def __call__(self, command) -> type(MathNode):
        print(f"{command=}")
        if command == "frac":
            return Fraction
        elif command == "sqrt":
            return Root
        elif command == "text":
            return Text
        elif command == "sum":
            return Sum
        elif command == "diff":
            return Diff
        elif command == "int":
            return Integral
        elif command == "log":
            return Log
        elif command == ["sin", "cos", "tan", "ln", "lg"]:
            return Function
        elif command in ["pi", "e"]:
            return Constant
        elif command in ["alpha", "beta", "gamma", "varepsilon"]:
            return Symbol
        else:
            if self.cmdrules is None:
                return Symbol
            if self.cmdrules.get(command, None) is None:
                return Symbol
            else:
                return self.cmdrules.get(command)
