from mathnode.MathNode import (
    MathNode
)

OPEN = 0
CLOSE = 1

forbidden = {
    'd': "derivative symbol"
}

implemented = {
    'frac': ('fraction', 'mathnode.Fraction'),
    'sqrt': ('square root or cube root if used with sqrt[3] etc', 'mathnode.Root'),
    'int': ('integral', 'mathnode.Integral'),
    'diff': ('differential / derivative', 'mathnode.Diff'),
    'sin': ('sine', 'mathnode.Function'),
    'cos': ('cosine', 'mathnode.Function'),
    'tan': ('tangent', 'mathnode.Function'),
    'log': ('logarithm', 'mathnode.log'),
    'ln': ('logarithm base e', 'mathnode.Function'),
    'lg': ('logarithm base 10', 'mathnode.Function'),
    'pi': ('Pi (3.14159)', 'mathnode.Symbol'),
    'e': ('euler nr (2.71...)', 'mathnode.Symbol')
}

aliases = {
    'frac': 'fraction|frac',
    'sqrt': 'square root|sqrt|cbrt',
    'int': 'int|integral|primitive',
    'diff': 'diff|derivative|deriv',
    'sin': 'sin|sine|sinus',
    'cos': 'cos|cosine|cosinus',
    'tan': 'tan|tangenr',
    'log': 'log|logarithm',
    'lg': 'lg|base 10 log',
    'ln': 'ln|natural logarithm',
}

def get_aliases(f):
    return list(set([f] + list(aliases.get(f, f).split('|'))))

parantheses_map = {
    '{': '}',
    '[': ']',
    '(': ')'
}

import hashlib

def hamming(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

def hamming2(chaine1, chaine2):
    if isinstance(chaine2, list):
        return min(hamming2(chaine1, elem) for elem in chaine2)
    return len(list(filter(lambda x : ord(x[0])^ord(x[1]), zip(chaine1, chaine2))))


class Help:
    def __init__(self, type='all'):
        self.type = type
    
    def _help_to_dict(self, object: MathNode):
        object_type = type(object)
        param_names = object.__dict__.keys()
        params = object.__dict__.values()
        example_latex = object_type.example_message
        return param_names, params, example_latex, object_type
    
    def _help_find(self, implementation: str, top=3, verbose=True):
        distances = [(hamming2(implementation, get_aliases(key)), key) for key, val in implemented.items()]
        distances = sorted(distances)[:top]
        found = [d[1] for d in distances]
        found = {k: v for k, v in implemented.items() if k in found}
        if verbose:
            for k, v in found.items():
                print(f"[*] {k}:\n\tDescription: {v[0]}\n\tFound in: {v[1]}\n\n")
        return found
