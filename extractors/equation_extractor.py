import re


def extract_math_sections(text):
    # Regex patterns for $, $$, and \[ \]
    pattern_inline = r"\$(?!\$)(.+?)(?<!\$)\$"
    pattern_display = r"\$\$(.+?)\$\$"
    pattern_brackets = r"\\\[(.+?)\\\]"

    matches = (
        re.findall(pattern_inline, text, re.DOTALL)
        + re.findall(pattern_display, text, re.DOTALL)
        + re.findall(pattern_brackets, text, re.DOTALL)
    )

    return [m.strip() for m in matches]


from mathnode import BinaryOperator


def classify_math(content):
    # Remove LaTeX commands and whitespace for analysis
    cleaned = re.sub(r"\\[a-zA-Z]+", "", content)  # Remove commands like \frac, \text
    cleaned = re.sub(r"\{.*?\}", "", content)  # Remove contents of brackets
    cleaned = cleaned.replace(" ", "")
    print(f"{cleaned=}")
    # Classification
    _all_list = ["\\" + x for x in BinaryOperator.OPERATORS[1]] + ["=", ">", "<", ">=", "<="]
    print(f"{_all_list}")
    if any(op in cleaned for op in _all_list):
        print(f"\t=>eq!")
        return "equation"
    elif re.fullmatch(r"[a-zA-Z0-9\\]+", cleaned):
        return "symbol"
    else:
        return "expression"


def extract_and_classify_latex_math(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    math_sections = extract_math_sections(content)

    classified = []
    for m in math_sections:
        classification = classify_math(m)
        classified.append((m, classification))

    return classified
