from sympy import solve, parse_expr
from optimizations.logical_sentinel_finder import convert_inequality_to_interval,find_ultimate
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

def equation_solve(expression, sub_tree):
    """Solve Equation."""
    import re
    c_int_max = 2147483647
    if(re.search("[&|]", expression)):
        convert_inequality_to_interval(0, len(sub_tree), sub_tree)
        res = find_ultimate(0, len(sub_tree), sub_tree)
        print("\n in eq solve\n", sub_tree)
        for sentinel_interval in sub_tree[0]:
            lower = sentinel_interval[0]
            upper = sentinel_interval[1]
            sentinel_value = (lower + upper)//2
            if(upper - lower > 1):
                if(sentinel_value<-1 * c_int_max):
                    return str(-1 * c_int_max)
                elif(sentinel_value> c_int_max):
                    return str(c_int_max)
                return str(sentinel_value)
        return None
    else:
        # finds feasible point satisfying expression and inequality
        def satisfy(crit_point):
            point_1 =  "(" + str(crit_point) + "- 1)"
            point_2 =  "(" + str(crit_point) + "+ 1)"
            modified_expression = re.sub("[A-Za-z_][A-Za-z0-9_]*", point_1, expression)
            if(parse_expr(modified_expression, evaluate=True)):
                return point_1
            return point_2

        # op = r"(?:<|>|(?:<=)|(?:>=)|(?:==)|(?:!=))"
        op_eq = "(?:(?:==)|(?:<=)|(?:>=))"
        lhs_pat = r"([^\s]+?)"
        rhs_pat = "([^\s]+?)"
        pat = lhs_pat + op_eq + rhs_pat
        print(expression)
        m = re.search(pat, expression)
        critical_point = None
        # If there is =
        if(m):
            lhs, rhs = m.group(1), m.group(2)
            print("lhs rhs", lhs, rhs)
            new_expression = lhs + '-' + '(' + rhs + ')'
            critical_point = solve(parse_expr(new_expression, evaluate=True))[0]
        else:
            op_neq = "(?:(?:<)|(?:>)|(?:!=))"
            pat = lhs_pat + op_neq + rhs_pat
            m = re.search(pat, expression)
            if(m):
                print("Going in")
                lhs, rhs = m.group(1), m.group(2)
                print("lhs rhs", lhs, rhs)
                new_expression = lhs + '-' + '(' + rhs + ')'
                critical_point = solve(parse_expr(new_expression, evaluate=True))[0]
                return parse_expr(satisfy(critical_point))

        return str(critical_point)
