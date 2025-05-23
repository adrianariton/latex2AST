This converts a latex expression to an AST which can then be converted to any language by creating the to_<language> implementations in the MathNode class and its inheritors.

to run:
```sh
python3 index.py <document_path_or_index>
```

Example:
```sh
python3.11 index.py 1
# -------- output ----------
Data:

m > 0: is a/an equation

Wolfram Equation: Greater[m, 0]
Z3 Equation: m > 0
        - added to z3 context!
---------------------------

F: is a/an symbol

Wolfram Equation: F
Z3 Equation: F
---------------------------

m: is a/an symbol

Wolfram Equation: m
Z3 Equation: m
---------------------------

a: is a/an symbol

Wolfram Equation: a
Z3 Equation: a
---------------------------

m: is a/an symbol

Wolfram Equation: m
Z3 Equation: m
---------------------------

v: is a/an symbol

Wolfram Equation: v
Z3 Equation: v
---------------------------

h: is a/an symbol

Wolfram Equation: h
Z3 Equation: h
---------------------------

g \approx 9.81~\text{m/s}^2: is a/an equation

Wolfram Equation: Equals[g, 9.81]
Z3 Equation: g == 981/100
        - added to z3 context!
---------------------------

\Delta U: is a/an symbol

Wolfram Equation: Delta[U]
Z3 Equation: Delta_U
---------------------------

Q: is a/an symbol

Wolfram Equation: Q
Z3 Equation: Q
---------------------------

W: is a/an symbol

Wolfram Equation: W
Z3 Equation: W
---------------------------

\Delta S = 0: is a/an equation

Wolfram Equation: Equals[Delta[S], 0]
Z3 Equation: Delta_S == 0
        - added to z3 context!
---------------------------

S: is a/an symbol

Wolfram Equation: S
Z3 Equation: S
---------------------------

F = ma: is a/an equation

Wolfram Equation: Equals[F, Construct[m, a]]
Z3 Equation: F == m*a
        - added to z3 context!
---------------------------

E_k = \frac{1}{2}mv^2: is a/an equation

Wolfram Equation: Equals[Subscript[E, k], Construct[Construct[Multiply[1, Inv[2]], m], Power[v, 2]]]
Z3 Equation: E_k == 1/2*m*v**2
        - added to z3 context!
---------------------------

E_p = mgh: is a/an equation

Wolfram Equation: Equals[Subscript[E, p], Construct[Construct[m, g], h]]
Z3 Equation: E_p == m*g*h
        - added to z3 context!
---------------------------

\Delta U = Q - W: is a/an equation

Wolfram Equation: Equals[Delta[U], Plus[Q, Times[-1, W]]]
Z3 Equation: Delta_U == Q - W
        - added to z3 context!
---------------------------

\Delta S \geq 0: is a/an equation

Wolfram Equation: GreaterOrEqual[Delta[S], 0]
Z3 Equation: Delta_S >= 0
        - added to z3 context!
---------------------------

\lim_{T \to 0} S = S_0: is a/an equation

Wolfram Equation: Equals[Lim[To[T, 0],S], Subscript[S, 0]]
Z3 Equation: None
        - equation has no valid z3 form
---------------------------

Z3 Says...
documents/latex_document.tex is sat
```

```sh
python3.11 index.py documents/kirchoff_document_error.tex # or 3 instead of the path
# ------- output -------

Data:

R_1 = 2: is a/an equation

Wolfram Equation: Equals[Subscript[R, 1], 2]
Z3 Equation: R_1 == 2
        - added to z3 context!
---------------------------

R_2 = 3: is a/an equation

Wolfram Equation: Equals[Subscript[R, 2], 3]
Z3 Equation: R_2 == 3
        - added to z3 context!
---------------------------

R_3 = 5: is a/an equation

Wolfram Equation: Equals[Subscript[R, 3], 5]
Z3 Equation: R_3 == 5
        - added to z3 context!
---------------------------

V - V_{1} - V_{2} - V_{3} = 0: is a/an equation

Wolfram Equation: Equals[Plus[Plus[Plus[V, Times[-1, Subscript[V, 1]]], Times[-1, Subscript[V, 2]]], Times[-1, Subscript[V, 3]]], 0]
Z3 Equation: V - V_1 - V_2 - V_3 == 0
        - added to z3 context!
---------------------------

V_{1} = I R_1: is a/an equation

Wolfram Equation: Equals[Subscript[V, 1], Construct[I, Subscript[R, 1]]]
Z3 Equation: V_1 == I*R_1
        - added to z3 context!
---------------------------

V_{2} = I R_2: is a/an equation

Wolfram Equation: Equals[Subscript[V, 2], Construct[I, Subscript[R, 2]]]
Z3 Equation: V_2 == I*R_2
        - added to z3 context!
---------------------------

V_{3} = I R_3: is a/an equation

Wolfram Equation: Equals[Subscript[V, 3], Construct[I, Subscript[R, 3]]]
Z3 Equation: V_3 == I*R_3
        - added to z3 context!
---------------------------

10 - 2I - 3I - 5I + I R_3 = 0: is a/an equation

Wolfram Equation: Equals[Plus[Plus[Plus[Plus[10, Times[-1, Construct[2, I]]], Times[-1, Construct[3, I]]], Times[-1, Construct[5, I]]], Construct[I, Subscript[R, 3]]], 0]
Z3 Equation: 10 - 2*I - 3*I - 5*I + I*R_3 == 0
        - added to z3 context!
---------------------------

10 - 10I = 0: is a/an equation

Wolfram Equation: Equals[Plus[10, Times[-1, Construct[10, I]]], 0]
Z3 Equation: 10 - 10*I == 0
        - added to z3 context!
---------------------------

I = 1: is a/an equation

Wolfram Equation: Equals[I, 1]
Z3 Equation: I == 1
        - added to z3 context!
---------------------------

V_{1} = 1 \times 2: is a/an equation

Wolfram Equation: Equals[Subscript[V, 1], Times[1, 2]]
Z3 Equation: V_1 == 2
        - added to z3 context!
---------------------------

V_{2} = 1 \times 3: is a/an equation

Wolfram Equation: Equals[Subscript[V, 2], Times[1, 3]]
Z3 Equation: V_2 == 3
        - added to z3 context!
---------------------------

V_{3} = 1 \times 5: is a/an equation

Wolfram Equation: Equals[Subscript[V, 3], Times[1, 5]]
Z3 Equation: V_3 == 5
        - added to z3 context!
---------------------------

Z3 Says...
documents/kirchoff_document_error.tex is unsat
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



## Z3

- [ ]: TODO: 
    - implement logic from [https://ericpony.github.io/z3py-tutorial/advanced-examples.htm](https://ericpony.github.io/z3py-tutorial/advanced-examples.htm)