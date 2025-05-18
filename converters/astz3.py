from z3 import *
from mathnode import *


class Z3Context:
    def __init__(self):
        self.solver = Solver()

    def parse(self, node: MathNode):
        pass
