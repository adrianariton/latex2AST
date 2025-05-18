from z3 import *
from mathnode import *


class Z3Context:
    def __init__(self):
        self.solver = Solver()

    def add(self, node: MathNode):
        try:
            z3_node = node.to_z3()
        except Exception as e:
            print(f"""Could not convert {node.to_latex()} to z3:\n\t{e.with_traceback()}""")
            return

        self.solver.add(z3_node)

    def check(self):
        return self.solver.check()
