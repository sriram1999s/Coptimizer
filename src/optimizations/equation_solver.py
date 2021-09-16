from sympy import solve, parse_expr 

def flatten(l):
    """Eliminates the nested nature of an iterable for convenient processing."""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


# new_expression = "x-1"
# solution = solve(parse_expr(new_expression,evaluate=True))
# print(solution)

def equation_solve(expression):
    """Solve Equation."""
    import re
    # op = r"(?:<|>|(?:<=)|(?:>=)|(?:==)|(?:!=))"
    pat = r"([^\s]+?)==([^\s]+?)"
    print(expression)
    m = re.search(pat, expression)
    critical_point = None
    if(m):
        lhs, rhs = m.group(1), m.group(2)
        new_expression = lhs + '-' + '(' + rhs + ')'
        critical_point = solve(parse_expr(new_expression, evaluate=True))[0]
    return str(critical_point)
