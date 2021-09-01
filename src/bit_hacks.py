from parser_file import flatten


def validate_find_min(sub_tree):
    # print('sub tree0', sub_tree[0]) # if
    # print('sub tree1', sub_tree[1]) # [if_condition, if_body]
    # print('sub tree2', sub_tree[2]) # else
    # print('sub tree3', sub_tree[3]) # else_body

    if_condition = list(flatten(sub_tree[1][0]))
    lhs, op, rhs = is_min_condition(if_condition)
    if lhs is not None:
        res_var = is_min_body1(lhs, list(flatten(sub_tree[1][1])))
        if res_var:
            if is_min_body2(res_var, rhs, list(flatten(sub_tree[3]))):
                sub_tree = [res_var, '=', rhs, '^', '((', lhs, '^', rhs, ')', '&', '-', '(', lhs, '<', rhs, '))', ';']
    return sub_tree


def is_min_condition(condition):
    i = 0
    while i < len(condition):
        if condition[i] != '(':
            break
        i += 1
    while i < len(condition):
        if condition[i] == '<' or condition[i] == '<=':
            j = condition.index(')')
            while j > i and j < len(condition):
                if condition[j] != ')':
                    return (None, None, None)
                j += 1
            lhs = condition[i - 1]
            op = condition[i]
            rhs = condition[i + 1]
            return (lhs, op, rhs)

        elif condition[i] == '>' or condition[i] == '>=':
            j = condition.index(')')
            while j > i and j < len(condition):
                if condition[j] != ')':
                    return (None, None, None)
                j += 1
            lhs = condition[i + 1]
            op = condition[i]
            rhs = condition[i - 1]
            return (lhs, op, rhs)
        i += 1
    return (None, None, None)


# need to check if type of s not float
def is_valid_res_var(s):
    import re
    if re.match("^[a-zA-Z0-9_]*$", s):
        return True
    return False


def is_min_body1(lhs, body):
    """if the body has any statement other than assignment statement"""
    if len(body) != 6:
        return False

    assignment_op_pos = body.index('=')
    if assignment_op_pos != -1:
        if assignment_op_pos + 1 < len(body) and body[assignment_op_pos + 1] == lhs:
            if is_valid_res_var(body[assignment_op_pos - 1]):
                return body[assignment_op_pos - 1]
    return False


def is_min_body2(res_var, rhs, body):
    """if the body has any statement other than assignment statement"""
    if len(body) != 6:
        return False

    assignment_op_pos = body.index('=')
    if assignment_op_pos != -1:
        if assignment_op_pos + 1 < len(body) and body[assignment_op_pos + 1] == rhs and body[
            assignment_op_pos - 1] == res_var:
            return True
    return False
