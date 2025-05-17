from mathnode.parser import latex_to_tree
from mathnode.utils import Help
from mathnode.Rule import LaTeX_Additional_Rules
import re

if __name__ == "__main__":
    # latex_equation = (
    #     r"2\iiint_{2}^{3} \iint_{a} \iint^{b} a + b + \transpose A d x d y d a d b + 3 d s d t d u"
    # )
    # latex_equation = r"2\int_{2}^{3} a + b + \transpose A dx"
    # latex_equation = r"C_{\text{eq}} = \frac{Q_{\text{total}}}{V} = \sum_{i=1}^{n} {C_i}"
    latex_equation = r"C_{\text{eq}} = \frac{Q}{Q * \sum_{i=1}^{n} \frac{1}{C_i}} = (\sum_{i=1}^{n} \frac{1}{C_i})^{1}"
    # latex_equation = r"U = \frac{1}{2} * \varepsilon * E^2 * A * d"
    parse_tree, tokens = latex_to_tree(latex_equation, rules=LaTeX_Additional_Rules)
    print("\n\n")
    print(tokens)
    print("\n")
    print("Generated Wolfram:", parse_tree.to_wolfram())
