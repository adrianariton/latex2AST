from mathnode import *
from mathnode.utils import parantheses_map, OPEN, CLOSE, forbidden
from mathnode.From import CommandFrom


class Tokenizer:
    def __init__(self, latex_str):
        self.latex_str = latex_str
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.latex_str):
            current_char = self.latex_str[self.pos]

            if current_char.isspace():
                self.pos += 1
                continue

            if current_char == "\\":
                self.pos += 1
                cmd = []
                while self.pos < len(self.latex_str) and self.latex_str[self.pos].isalpha():
                    cmd.append(self.latex_str[self.pos])
                    self.pos += 1
                comm = "".join(cmd)
                if not BinaryOperator.is_operator(comm):
                    self.tokens.append(("COMMAND", "".join(cmd)))
                else:
                    self.tokens.append(("OPERATOR", "".join(cmd)))

            elif current_char in ("{", "}", "[", "]", "^", "_"):
                self.tokens.append((current_char, current_char))
                self.pos += 1
            elif current_char.isalpha():
                self.tokens.append(("SYMBOL", current_char))
                self.pos += 1
            elif current_char.isdigit() or current_char == ".":
                num = []
                while self.pos < len(self.latex_str) and (
                    self.latex_str[self.pos].isdigit() or self.latex_str[self.pos] == "."
                ):
                    num.append(self.latex_str[self.pos])
                    self.pos += 1
                self.tokens.append(("CONSTANT", "".join(num)))
            else:
                self.tokens.append(("OPERATOR", current_char))
                self.pos += 1
        return self.tokens


class Parser:
    def __init__(self, tokens, cmdrules: dict[MathNode] = None):
        self.tokens = tokens
        self.pos = 0
        self.inserted_pos = 0
        self.rules = cmdrules

    # TODO: mai multe litere
    @property
    def real_pos(self):
        return self.pos - self.inserted_pos

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        return self.parse_binary_order()

    def parse_apply_function(self):
        left = self.parse_term()
        while self.pos < len(self.tokens):
            token_type, token_value = self.current_token()
            if token_value == "(":
                self.consume_token()
                right = self.parse_expression()
                left = Apply(left, right)
                self.expect_current(")")
                self.consume_token()
            elif (
                token_type == "SYMBOL" or token_type == "COMMAND"
            ) and token_value not in forbidden.keys():
                if isinstance(left, Constant):
                    right = self.parse_term()
                    left = Apply(left, right)
                elif token_type != "COMMAND":
                    right = self.parse_term()
                    left = Apply(left, right)  ## aici
                else:
                    break
            else:
                break
        return left

    def parse_binary_order(self, order=0):
        if order >= len(BinaryOperator.OPERATORS):
            return self.parse_apply_function()
        left = self.parse_binary_order(order + 1)
        while self.pos < len(self.tokens):
            token_type, token_value = self.current_token()
            if token_value in BinaryOperator.OPERATORS[order]:
                self.consume_token()
                right = self.parse_binary_order(order + 1)
                left = BinaryOperator(token_value, left, right)
            else:
                break
        return left

    def parse_term(self):
        node = self.parse_factor()
        while self.pos < len(self.tokens):
            token_type, token_value = self.current_token()
            if token_value in ["_"]:
                self.consume_token()
                subscript = self.parse_subscript()
                node = Subscript(node, subscript)
            elif token_value in ["^"]:
                self.consume_token()
                subscript = self.parse_subscript()
                node = Superscript(node, subscript)
            else:
                break
        return node

    def expect_current(self, expect, message=None):
        if message is None:
            message = ""

        message = f"\n--------------------------\nExpected {expect} @ #token={self.real_pos}\nleft_to_check={self.tokens[self.pos:]}\n\t[*] Additional message: \n\t{message}"
        assert self.current_token()[1] == expect, message

    def expect_current_any(self, expect, message=None):
        if message is None:
            message = ""

        message = f"\n--------------------------\nExpected {expect} @ #token={self.real_pos}\nleft_to_check={self.tokens[self.pos:]}\n\t[*] Additional message: \n\t{message}"
        assert self.current_token()[1] in expect, message

    def parse_factor(self):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")

        token_type, token_value = self.current_token()

        if token_type == "COMMAND":
            return self.parse_command()
        elif token_type == "SYMBOL":
            self.consume_token()
            return Symbol(token_value)
        elif token_type == "CONSTANT":
            self.consume_token()
            return Constant(token_value)
        elif token_value == "{":
            self.consume_token()
            content = self.parse_expression()
            self.expect_current("}")
            self.consume_token()
            return content
        elif token_value == "(":
            self.consume_token()
            content = self.parse_expression()
            self.expect_current(")")
            self.consume_token()
            return content
        else:
            self.consume_token()
            return Symbol(token_value) if token_type == "OPERATOR" else Symbol(token_value)

    def parse_command(self):
        command = self.current_token()[1]
        self.consume_token()
        cmd_object = CommandFrom(self.rules)(command)
        return cmd_object.consume(self, command)

    def begin_expression(self, separator="{"):
        self._insert_after_current_token(separator)

    def parse_argument(self, separator="{}"):
        if separator == "Any":
            current = self.current_token()[1]
            print(f"current={current}")
            last = parantheses_map.get(current, None)
            print(f"{last=}")
            if last is None:
                # probably symbol
                return self.parse_term()
            self.expect_current(current)
            self.consume_token()
            arg = self.parse_expression()
            self.expect_current(last)
            self.consume_token()
            return arg

        self.expect_current(separator[OPEN])
        self.consume_token()
        arg = self.parse_expression()
        self.expect_current(separator[CLOSE])
        self.consume_token()
        return arg

    def jump_back(self):
        if self.pos > 0:
            self.pos -= 1

    def parse_term_until(self, separator="d"):
        self.begin_expression()
        expresion = self.parse_argument(f"{'{'}{separator}")
        return expresion

    def print_left(self):
        print(f"left_to_check={self.tokens[self.pos:]}")

    def parse_exponent(self):
        if self.current_token()[1] == "{":
            self.consume_token()
            exp = self.parse_expression()
            self.expect_current("}")
            self.consume_token()
            return exp
        else:
            return self.parse_factor()

    def parse_subscript(self):
        if self.current_token()[1] == "{":
            self.consume_token()
            sub = self.parse_expression()
            self.expect_current("}")
            self.consume_token()
            return sub
        else:
            return self.parse_factor()

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def peek_token(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else (None, None)

    def _insert_after_current_token(self, new_token):
        self.inserted_pos += 1
        self.tokens.insert(self.pos, (new_token, new_token))

    def consume_token(self):
        if self.pos < len(self.tokens):
            self.pos += 1


def latex_to_tree(latex_str, rules: list[MathNode]):
    tokenizer = Tokenizer(latex_str)
    tokens = tokenizer.tokenize()
    print(tokens)
    parser = Parser(tokens, cmdrules=rules)
    return parser.parse(), tokens
