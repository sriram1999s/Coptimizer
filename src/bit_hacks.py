from parser_file import flatten


def validate_find_min(sub_tree):
    # print('sub tree0', sub_tree[0]) # if
    # print('sub tree1', sub_tree[1]) # [if_condition, if_body]
    # print('sub tree2', sub_tree[2]) # else
    # print('sub tree3', sub_tree[3]) # else_body

    if_condition = [str(i) for i in list(flatten(sub_tree[1][0]))]
    lhs, op, rhs = is_min_condition(if_condition)
    if lhs is not None:
        if_body = [str(i) for i in list(flatten(sub_tree[1][1]))]
        res_var = is_min_body1(lhs, if_body)
        if res_var:
            else_body = [str(i) for i in list(flatten(sub_tree[3]))]
            if is_min_body2(res_var, rhs, else_body):
                sub_tree = [res_var, '=', rhs, '^', '((', lhs, '^', rhs, ')', '&', '-', '(', lhs, '<', rhs, '))', ';']
    return sub_tree


'''check if the condition is of the form x<y or x<=y or y>x or y>=x'''
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
            indices = [i for i, x in enumerate(condition) if x == "("]
            lhs = ''.join(flatten(condition[indices[-1] + 1: i]))
            op = condition[i]
            rhs = ''.join(flatten(condition[i + 1: condition.index(')')]))
            return (lhs, op, rhs)

        elif condition[i] == '>' or condition[i] == '>=':
            j = condition.index(')')
            while j > i and j < len(condition):
                if condition[j] != ')':
                    return (None, None, None)
                j += 1
            lhs = ''.join(flatten(condition[i + 1: condition.index(')')]))
            op = condition[i]
            indices = [i for i, x in enumerate(condition) if x == "("]
            rhs = ''.join(flatten(condition[indices[-1] + 1: i]))
            return (lhs, op, rhs)
        i += 1
    return (None, None, None)


# need to check if type of s not float
def is_valid_res_var(s):
    import re
    if re.match("^[a-zA-Z0-9_]*$", s):
        return True
    return False


'''check if body of if is of the form r=x'''
def is_min_body1(lhs, body):
    """if the body has any statement other than assignment statement"""
    indices = [i for i, x in enumerate(body) if x == ";"]
    if len(indices) > 1:
        return False

    try:
        assignment_op_pos = body.index('=')
        if ''.join(flatten(body[assignment_op_pos + 1: indices[0]])) == lhs:
            res_var = ''.join(flatten(body[body.index('{') + 1:assignment_op_pos]))
            return res_var
        return False
    except ValueError:
        return False


'''check if the body is of else is f the form r=y'''
def is_min_body2(res_var, rhs, body):
    """if the body has any statement other than assignment statement"""
    indices = [i for i, x in enumerate(body) if x == ";"]
    if len(indices) > 1:
        return False

    try:
        assignment_op_pos = body.index('=')
        if ''.join(flatten(body[assignment_op_pos + 1: indices[0]])) == rhs and ''.join(
                flatten(body[body.index('{') + 1:assignment_op_pos])) == res_var:
            return True
        return False
    except ValueError:
        return False


'''flattens and converts non-list elements to string'''
def flatten1(L):
    for l in L:
        if isinstance(l, list):
            yield from flatten1(l)
        else:
            yield str(l)


'''change (x+y)%n to (x+y) - (n& -((x+y) >= n))'''
def validate_compute_mod(sub_tree):
    import re
    flattened_sub_tree = ''.join(flatten1(sub_tree))
    pat = '\(+[a-zA-Z_\-0-9]+\+[a-zA-Z_\-0-9]+\)+%\(*[a-zA-Z_\-0-9]+\)*$'
    pat_sum = '^\(+[a-zA-Z_\-0-9]+\+[a-zA-Z_\-0-9]+\)+'
    pat_n = '\(*[a-zA-Z_\-0-9]+\)*$'
    m = re.search(pat, flattened_sub_tree)
    if m:
        expression = m.group(0)
        m = re.search(pat_sum, expression)
        if m:
            sum1 = m.group(0)
            m = re.search(pat_n, expression)
            if m:
                n = m.group(0)
                before_expression = flattened_sub_tree.find(expression)
                if before_expression != -1:
                    ret = flattened_sub_tree[
                          :before_expression] + sum1 + '-' + '(' + n + '&' + '-' + '(' + sum1 + '>=' + n + '))'
                    return ret
    return sub_tree


'''converts any call to abs function to bit hack'''
def validate_find_abs(tree):
    import secrets
    flattened_tree = list(flatten(tree))
    i = 0
    mask_pos = -1
    need_header = False
    while i < len(flattened_tree):

        '''mask will be created before the statement that contains the call to abs'''
        if flattened_tree[i] in ['{', '}', ')', ';']:
            mask_pos = i+1
            i += 1

        elif flattened_tree[i] == 'abs' and flattened_tree[i+1] == '(':
            need_header = True
            open_paran = 1
            j = i+2
            var = ''
            while j < len(flattened_tree) and open_paran:
                if flattened_tree[j] == ')':
                    open_paran -= 1
                    if open_paran == 0:
                        break
                elif flattened_tree[j] == '(':
                    open_paran += 1
                var += str(flattened_tree[j])
                j += 1
            hash = secrets.token_hex(nbytes=4)
            new_code = f'int const mask{hash} = {var} >> sizeof(int) * CHAR_BIT - 1;'
            flattened_tree.insert(mask_pos, new_code)
            new_code = f'({var} + mask{hash}) ^ mask{hash}'

            """
            Since we have added f'#include<limits.h>\nint const mask{hash} = {var} >> sizeof(int) * CHAR_BIT - 1;'
            , all the elements after mask_pos are shifted by 1
            """
            flattened_tree[i+1:j+1] = ''
            flattened_tree[i+1] = new_code

            # i = flattened_tree.index(new_code) + 1
            i += 2

        else:
            i += 1

    if need_header:
        flattened_tree.insert(0, '#include<limits.h>\n')
    return flattened_tree




