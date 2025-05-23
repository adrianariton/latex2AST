from mathnode.parser import latex_to_tree
from mathnode.utils import Help
from mathnode.Rule import LaTeX_Additional_Rules
import re
from converters.astz3 import Z3Context
from extractors.equation_extractor import extract_and_classify_latex_math
import sys
import os


def get_tex_files(folder="documents"):
    tex_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".tex"):
                path = os.path.join(root, file).replace("\\", "/")
                tex_files.append(path)
    return tex_files


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    document_path = "documents/latex_document.tex"
    available_docs = get_tex_files()
    args = sys.argv[1:]
    if len(args) > 0:
        document_path = str(args[0])
        if is_int(document_path):
            assert int(document_path) < len(available_docs)
            document_path = available_docs[int(document_path)]
        assert document_path in available_docs, f"Document should be in {available_docs}"

    document_equations = extract_and_classify_latex_math(document_path)

    print(document_equations)
    print("\n\n=====================")
    eqs = []
    for latex_eq, _type in document_equations:
        wolfram_eq = None
        z3_eq = None
        print(f"{latex_eq=} :{_type}")
        parse_tree, tokens = latex_to_tree(latex_eq, rules=LaTeX_Additional_Rules)
        try:
            wolfram_node = parse_tree.to_wolfram()
            wolfram_eq = wolfram_node
            print("Generated Wolfram:", wolfram_node)
        except Exception as e:
            print("Could not convert to wolfram")
        try:
            z3_node = parse_tree.to_z3()
            print("Generated Z3:", z3_node)
            z3_eq = z3_node
        except Exception as e:
            print(
                "Could not convert to z3, try only with polynomials and algebraic numbers and ops, ie no sin cos derivs integrals"
            )
        eqs += [(latex_eq, _type, wolfram_eq, z3_eq)]
        print("---------------------------\n")
    print("\n\n\nData:\n")

    context = Z3Context()
    for leq, _type, weq, zeq in eqs:
        print(f"{leq}: is a/an {_type}\n")
        print(f"Wolfram Equation: {weq}")
        print(f"Z3 Equation: {zeq}")
        if _type == "equation":
            if zeq is not None:
                print("\t- added to z3 context!")
                context.add(zeq)
            else:
                print("\t- equation has no valid z3 form")
        print("---------------------------\n")

    print(f"Z3 Says...")
    print(f"{document_path} is {context.check()}")

    # exit(0)
    # # latex_equation = (
    # #     r"2\iiint_{2}^{3} \iint_{a} \iint^{b} a + b + \transpose A d x d y d a d b + 3 d s d t d u"
    # # )
    # # latex_equation = r"2\int_{2}^{3} a + b + \transpose A dx"
    # # latex_equation = r"C_{\text{eq}} = \frac{Q_{\text{total}}}{V} = \sum_{i=1}^{n} {C_i}"
    # # latex_equation = r"C_{\text{eq}} = \frac{Q}{Q * \sum_{i=1}^{n} \frac{1}{C_i}} = (\sum_{i=1}^{n} \frac{1}{C_i})^{1}"
    # latex_equation = r"\lim_{x \to 0} {x}"
    # # complicated equations work with only wolfram for now
