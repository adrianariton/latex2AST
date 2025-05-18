This converts a latex expression to an AST which can then be converted to any language by creating the to_<language> implementations in the MathNode class and its inheritors.

to run:
```
python3 index.py
```

if some latex rules are not **yet** implemented, they can be specified in `mathnode/Rule.py` in this dictionary:

```py
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
## add here your rules
}
```

for example if i wanted a rule for a function that would look like:

```\nabla^{power}``` f, where power is 10 if unspecified

i would add:
```py
"nabla": abstract_rule_from("\\nabla?^{@power|10} ?{f}", function_name='nabla') ## double slash to escape the slash
```
where ? marks the power as optional and the accolades around f as optional as well.

