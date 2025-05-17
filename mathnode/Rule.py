from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathnode.parser import Parser
from mathnode.MathNode import MathNode
from mathnode.Constant import Constant
from mathnode.Integral import Integral
from mathnode.utils import forbidden


def is_var_char(c):
    return c.isalpha() or c == "\\" or c == "|" or c == "_" or c.isdigit()


def isalnumnosep(c):
    return c.isalnum() and c not in forbidden.keys()


class CommandRule:
    OPEN_PARANTHESES = "{[("
    CLOSED_PARANTHESES = ")]}"
    SUBSUPERSCRIPTS = "_^*"
    MANIPULATORS = ",;:"
    ALL_OPERATORS = OPEN_PARANTHESES + CLOSED_PARANTHESES + SUBSUPERSCRIPTS + MANIPULATORS
    NO_PARANTHESES = SUBSUPERSCRIPTS + MANIPULATORS

    def __init__(self, regex: str, function_name: str, params: list[str]):
        self.regex = regex
        self.function_name = function_name
        self.params = params
        assert self.regex.startswith(
            f"\\{function_name}"
        ), "Rule function name should start with \\ followed by function name"

    def consume(self, parser: "Parser", command: str):
        regex = self.regex[len(f"\\{self.function_name}") :]

        i = 0

        def current_char():
            return regex[i]

        def peek_next_char():
            h = i + 1
            while regex[h] == "?" or regex[h] == "&":
                h += 1
            return regex[h], (regex[h - 1] == "?"), h

        print(f"{regex=}")
        params = {}
        is_optional = False
        can_miss_paran = True
        old_marker_match = True
        finish_char = None
        while i < len(regex):
            curr = current_char()
            if curr == " " or curr == "\t":
                i += 1
                continue
            if curr == "?":
                can_miss_paran = True
                is_optional = True
                old_marker_match = True
                i += 1
                continue
            if curr == "&":
                i += 1
                finish_char = current_char()
                i += 1
                continue
            if curr == "!":
                can_miss_paran = False
                i += 1
                continue
            print(
                f"\n{curr=} parser_curr={parser.current_token()[1]} {is_optional=} {old_marker_match=}"
            )
            if curr in CommandRule.SUBSUPERSCRIPTS:
                is_marker = parser.current_token()[1] in list(CommandRule.SUBSUPERSCRIPTS)

                if curr == parser.current_token()[1]:

                    # consume them and wait for expression
                    old_marker_match = True
                    print("Match!")
                else:
                    # if is_marker:
                    old_marker_match = False

                    print("Unmatch:  ", curr, parser.current_token()[1])

                if parser.current_token()[1] in list(CommandRule.OPEN_PARANTHESES):
                    old_marker_match = False

                variable, _, _ = peek_next_char()
                assert variable in list(
                    CommandRule.OPEN_PARANTHESES
                ), "After a SUBSUPERSCRIPTS there should be a parameter"
                if not is_optional:
                    parser.expect_current_any(curr, list(CommandRule.OPEN_PARANTHESES))

                if not old_marker_match:
                    while current_char() not in ["@"] and i < len(regex):
                        i += 1
                    if i >= len(regex):
                        break
                    i += 1
                    c = current_char()
                    assert c.isalpha(), f"variable should start w/ alpha character not {c}"
                    variable_name = ""
                    c = current_char()
                    while is_var_char(c) and i < len(regex):
                        variable_name += c
                        i += 1
                        c = current_char()

                    while current_char() in CommandRule.CLOSED_PARANTHESES and i < len(regex):
                        i += 1
                    if len(variable_name.split("|")) == 2:
                        variable_name, variable_default_value = variable_name.split("|")
                    else:
                        variable_name, variable_default_value = variable_name, "None"

                    if params.get(variable_name) == None:
                        params[variable_name] = Constant(variable_default_value)
                    old_marker_match = True
                    is_optional = False
                    can_miss_paran = False
                    finish_char = None
                    continue

                can_miss_paran = True
                i += 1
                print(f"{is_marker=}")
                if is_marker:
                    print(f"next! {parser.current_token()} -> ", end="")
                    parser.consume_token()
                    print(f"{parser.current_token()}\n")

            elif curr in CommandRule.OPEN_PARANTHESES:

                variable, _, new_i = peek_next_char()
                assert variable == "@", "Param names should start with '@'"
                variable_name = ""
                i = new_i
                i += 1
                c = current_char()
                while is_var_char(c) and i < len(regex):
                    variable_name += c
                    i += 1
                    c = current_char()
                while i < len(regex) and current_char() in CommandRule.CLOSED_PARANTHESES:
                    i += 1
                # ajung la paranteza inchisa acuma
                if len(variable_name.split("|")) == 2:
                    variable_name, variable_default_value = variable_name.split("|")
                else:
                    variable_name, variable_default_value = variable_name, "None"
                print(
                    "b",
                    variable_name,
                    variable_default_value,
                    is_optional,
                    old_marker_match,
                    f"{parser.current_token()[1]=}",
                )

                print(f"{can_miss_paran=}")
                if parser.current_token()[1] != curr:
                    if not can_miss_paran:
                        if params.get(variable_name) == None:
                            params[variable_name] = Constant(variable_default_value)

                        finish_char = None
                        continue
                    if can_miss_paran and not isalnumnosep(parser.current_token()[1]):
                        if params.get(variable_name) == None:
                            params[variable_name] = Constant(variable_default_value)

                        finish_char = None
                        continue

                if not is_optional:
                    assert old_marker_match == True, "Rule does not match"
                    if not can_miss_paran:
                        if finish_char is not None:
                            params[variable_name] = parser.parse_term_until(finish_char)
                        else:
                            params[variable_name] = parser.parse_argument("{}")
                    else:
                        print("any!1!")
                        if finish_char is not None:
                            params[variable_name] = parser.parse_term_until(finish_char)
                        else:
                            params[variable_name] = parser.parse_argument("Any")
                else:
                    if not old_marker_match:
                        if params.get(variable_name) == None:
                            params[variable_name] = Constant(variable_default_value)
                        print(f"default: {variable_name}:{variable_default_value}\n")
                    else:
                        if not can_miss_paran:
                            if finish_char is not None:
                                params[variable_name] = parser.parse_term_until(finish_char)
                            else:
                                params[variable_name] = parser.parse_argument("{}")
                        else:
                            print("any!2!")
                            if finish_char is not None:
                                params[variable_name] = parser.parse_term_until(finish_char)
                            else:
                                params[variable_name] = parser.parse_argument("Any")
                finish_char = None
                old_marker_match = True
                is_optional = False
                can_miss_paran = False
            elif curr == "@":
                variable = curr
                assert variable == "@", "Param names should start with '@'"
                variable_name = ""
                i += 1
                c = current_char()
                while is_var_char(c) and i < len(regex):
                    variable_name += c
                    i += 1
                    if i >= len(regex):
                        break
                    c = current_char()

                # ajung la paranteza inchisa acuma
                if len(variable_name.split("|")) == 2:
                    variable_name, variable_default_value = variable_name.split("|")
                else:
                    variable_name, variable_default_value = variable_name, "None"
                print("a", variable_name, variable_default_value, is_optional, old_marker_match)
                assert not is_optional, "Optional values can be only in accolades"
                if not is_optional:
                    print("any!!")
                    params[variable_name] = parser.parse_argument("Any")

                old_marker_match = True
                is_optional = False
                can_miss_paran = False
                finish_char = None
            else:
                i += 1
        return params


def _get_params_names(regex: str):
    i = 0
    params = []
    while i < len(regex):
        if regex[i] == "@":
            v_name = ""
            i += 1
            while i < len(regex) and is_var_char(regex[i]):
                v_name += regex[i]
                i += 1
            if len(v_name.split("|")) == 2:
                v_name, variable_default_value = v_name.split("|")
            else:
                v_name, variable_default_value = v_name, "None"

            params += [v_name]
        i += 1

    return params


def get_class_params(class_object: type[MathNode]):
    return [
        key
        for key, value in class_object.__dict__.items()
        if not key.startswith("__")
        and not callable(value)
        and not callable(getattr(value, "__get__", None))  # <- important
    ]


def abstract_rule_from_template(class_object: type[MathNode], function_name: str):
    class AbstractRuleNode(MathNode):
        def __init__(self, **kw_args):
            self.param_names = get_class_params(class_object)
            for k, v in kw_args.items():
                self.__dict__[k] = v
            self.param_dict = kw_args
            self.fname = function_name

        def to_latex(self):
            str_rep = {k: v.to_latex() for k, v in self.param_dict.items()}
            print("sdfsdf")
            return f"\\{function_name}({str_rep})"

        @staticmethod
        def consume(parser: "Parser", command: str):
            obj = class_object.consume(parser, command)
            obj.fname = function_name
            return obj

    return AbstractRuleNode


def abstract_rule_from(regex: str, function_name: str, params: list[str] | None = None):
    """A rule should follow the following parrern
    \\function_{@param}_{@param}..._{@param} {@param}{@param}{@param}...{@param}

    where instead of _ one can use *, _, or ^
    to make one param optional
    - if it is of the form _{@param}, one can replace it in the
    regex with ?_{@param|10} , where 10 can be replace with a default Constant value.

    - if it is of the form {@param}, one can replace it with:
        - ?{@param|10} if one wants to match both {expr} and x or default to 10 if not present (where x is a symbol and expr an expression)
        - ?!{@param|10} if one wants to match {expr} or default to 10 if not present

    for example \\func?_{@x|10} ?{@y} will match both \\func {2} and \\func_{3} {2} and \\func 2 and \\func_3 2

    Args:
        regex (str): _description_
        function_name (str): _description_

    Returns:
        _type_: _description_
    """
    if params is None:
        params = _get_params_names(regex)
    cmd_rule = CommandRule(regex, function_name, params)

    class AbstractRuleNode(MathNode):
        def __init__(self, **kw_args):
            self.fname = function_name
            self.param_names = params
            for k, v in kw_args.items():
                self.__dict__[k] = v
            self.param_dict = kw_args

        def to_latex(self):
            str_rep = {k: v.to_latex() for k, v in self.param_dict.items()}
            return f"\\{function_name}({str_rep})"

        def to_wolfram(self):
            str_rep = {k: v.to_wolfram() for k, v in self.param_dict.items()}
            return f"{function_name.title()}[{','.join(str_rep.values())}]"

        @staticmethod
        def consume(parser: "Parser", command: str):
            params_all = cmd_rule.consume(parser, command)
            return AbstractRuleNode(**params_all)

    return AbstractRuleNode


LaTeX_Additional_Rules = {
    "prod": abstract_rule_from(
        "\\prod_{@int_min}?^{@int_max|\\inf} ?{@expr|10}", function_name="prod"
    ),
    "sfrac": abstract_rule_from("\\sfrac{@den1}{@den2}?!{@expr}", function_name="sfrac"),
    "deriv": abstract_rule_from("\\deriv?*[@dtims|1]{@f}{@x}?!{@xexpr}", function_name="deriv"),
    "grad": abstract_rule_from("\\grad?{@f|0}", function_name="grad"),
    "laplace": abstract_rule_from("\\laplace?{@f|0}", function_name="laplace"),
    "binom": abstract_rule_from("\\binom{@n}{@k}", function_name="binom"),
    "vec": abstract_rule_from("\\vec?_{@i|1} ?{@x}", function_name="vec"),
    "norm": abstract_rule_from("\\norm?{@x}", function_name="norm"),
    "lim": abstract_rule_from("\\lim_{@vartoval}{@expr}", function_name="lim"),
    "transpose": abstract_rule_from("\\transpose?_{@A}?{@A}", function_name="transpose"),
    "inv": abstract_rule_from("\\inv?_{@f}?{@x|0}", function_name="inv"),
    "piecewise": abstract_rule_from("\\piecewise_{@x}?{@cond}?{@val|0}", function_name="piecewise"),
    # 'oint': abstract_rule_from_template(Integral, function_name='oint')
    "oint": abstract_rule_from(
        "\\oint?_{@int_min}?^{@int_max} &d ?{@expr} @deriv", function_name="oint"
    ),
    "oiint": abstract_rule_from(
        "\\oiint?_{@int_min}?^{@int_max} &d ?{@expr} &d ?{@x} ?{@y}", function_name="oiint"
    ),
    "oiiint": abstract_rule_from(
        "\\oiiint?_{@int_min}?^{@int_max} &d ?{@expr} &d ?{@x} &d ?{@y} ?{@z}",
        function_name="oiiint",
    ),
    "iint": abstract_rule_from(
        "\\iint?_{@int_min}?^{@int_max} &d ?{@expr} &d ?{@x} ?{@y}", function_name="iint"
    ),
    "iiint": abstract_rule_from(
        "\\iiint?_{@int_min}?^{@int_max} &d ?{@expr} &d ?{@x} &d ?{@y} ?{@z}", function_name="iiint"
    ),
}
