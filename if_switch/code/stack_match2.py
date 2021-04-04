class if_elif_else:
    # def __init__(self, type1, condition_vars):
    def __init__(self, type1, condition_vars, range_var=None, l=None, u=None, op1=None, op2=None):
        self.type1 = type1
        self.condition_vars = condition_vars

        self.l = l
        self.u = u
        self.op1 = op1
        self.op2 = op2
        self.range_var = range_var


dict_num_list_of_chains = dict()


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_char(s):
    # if len(s) == 1 and s.isalpha():
    #     return True
    # else:
    #     return False
    print('s', s)
    if s[0] == "'" and s[-1] == "'":
        return True
    return False


def identify_chains(z):
    global dict_num_list_of_chains
    window = []
    threshold = 0
    net_open = 0
    for i in range(len(z)):
        if z[i] == '{':
            net_open += 1

        elif z[i] == '}':
            net_open -= 1

        elif z[i] == 'if':
            obj = create_obj('if', i, z)
            if window == []:
                if net_open not in dict_num_list_of_chains.keys():
                    dict_num_list_of_chains[net_open] = [[obj]]

                    threshold = net_open

                else:
                    dict_num_list_of_chains[net_open].append([obj])
                if threshold < net_open:
                    threshold = net_open
            else:
                if net_open == threshold:
                    window = []
                    dict_num_list_of_chains[net_open].append([obj])
                elif net_open > threshold:
                    dict_num_list_of_chains[window[1]][-1].pop()
                    obj = create_obj('elif', i, z)
                    dict_num_list_of_chains[window[1]][-1].append(obj)
                    window = []
                else:
                    threshold = net_open
                    dict_num_list_of_chains[threshold].append([obj])
                    window = []

        elif z[i] == 'else':
            obj = create_obj('else', i, z)
            if net_open < threshold:
                # threshold = net_open
                threshold = find_prev_num(net_open)
            dict_num_list_of_chains[threshold][-1].append(obj)
            window = [(net_open, 'else'), threshold]


def create_obj(type1, pos, z):
    if type1 == 'if':
        # i = pos + 2
        # l = []
        #
        # while i < len(z) and z[i] == '(':
        #     i += 1
        # if i + 2 < len(z) and z[i + 1] == '==':
        #     if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i + 2]):
        #         # if after is || don't add var to list because should not switch
        #         if z[i + 3] != '||':
        #             l.append((z[i + 2], z[i]))
        #     elif (is_int(z[i + 2]) or is_char(z[i + 2])) and not is_int(z[i]):
        #         # if after is || don't add var to list because should not switch
        #         if z[i + 3] != '||':
        #             l.append((z[i], z[i + 2]))
        #
        # obj = if_elif_else('if', l)
        # return obj

        return util('if', z, pos+2)

    if type1 == 'elif':
        # i = pos + 2
        # l = []
        #
        # while i < len(z) and z[i] == '(':
        #     i += 1
        # if i + 2 < len(z) and z[i + 1] == '==':
        #     if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i + 2]):
        #         # if after is || don't add var to list because should not switch
        #         if z[i + 3] != '||':
        #             l.append((z[i + 2], z[i]))
        #             # l = (z[i + 2], z[i])
        #     elif (is_int(z[i + 2]) or is_char(z[i + 2])) and not is_int(z[i]):
        #         # if after is || don't add var to list because should not switch
        #         if z[i + 3] != '||':
        #             l.append((z[i], z[i + 2]))
        #             # l = (z[i], z[i + 2])
        #
        # obj = if_elif_else('elif', l)
        # return obj

        return util('elif', z, pos + 2)

    if type1 == 'else':
        obj = if_elif_else('else', None)
        return obj


def find_prev_num(num):
    global dict_num_list_of_chains
    ret = -1
    for i in dict_num_list_of_chains.keys():
        if i < num:
            ret = i
        elif i == num:
            ret = i
            break
        else:
            break
    # print('ret', ret)
    return ret


def skip_while(pos, ch, z):
    while pos<len(z) and z[pos] == ch:
        pos+=1
    return pos


def lateral_op(op):
    if op == '<':
        return '>'
    if op == '>':
        return '<'
    if op == '<=':
        return '>='
    if op == '>=':
        return '<='


def util(type1, z, i):
    l = []
    range_ops = ['<=', '>=', '<', '>']
    i = skip_while(i, '(', z)
    if i + 2 < len(z) and z[i + 1] == '==':
        if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i + 2]):
            # if after is || don't add var to list because should not switch
            if z[i + 3] != '||':
                l.append((z[i + 2], z[i]))
        elif (is_int(z[i + 2]) or is_char(z[i + 2])) and not is_int(z[i]):
            # if after is || don't add var to list because should not switch
            if z[i + 3] != '||':
                l.append((z[i], z[i + 2]))

    elif i + 7 < len(z) and z[i + 1] in range_ops:
        lower = None
        upper = None
        op1 = None
        op2 = None
        range_var = None

        # const
        if is_int(z[i]):
            lower = int(z[i])
        # var
        elif not is_int(z[i]):
            range_var = z[i]
        # other
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # op1
        if z[i] in range_ops:
            # const has been seen
            if lower is not None:
                op1 = z[i]
            # var has been seen
            elif range_var is not None:
                op1 = lateral_op(z[i])

        # other operator
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # const seen for the first time
        if is_int(z[i]) and lower is None:
            lower = int(z[i])
        # var seen for the first time
        elif not is_int(z[i]) and range_var is None:
            range_var = z[i]
        # other
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # other operator
        if z[i] != '&&':
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, '(', z)

        # const
        if is_int(z[i]):
            upper = int(z[i])
        # var
        elif not is_int(z[i]):
            if z[i] != range_var:
                obj = if_elif_else(type1, l)
                return obj
        # other
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # op2
        if z[i] in range_ops:
            # const has been seen
            if upper is not None:
                op2 = lateral_op(z[i])

            # var has been seen
            else:
                op2 = z[i]

        # other operator
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # const is seen for the first time
        if is_int(z[i]) and upper is None:
            upper = int(z[i])

        # var is seen for the first time
        elif not is_int(z[i]):
            if range_var != z[i]:
                obj = if_elif_else(type1, l)
                return obj
            else:
                pass
        # other
        else:
            obj = if_elif_else(type1, l)
            return obj

        i = skip_while(i + 1, ')', z)

        # more conditions
        if z[i] != '{':
            obj = if_elif_else(type1, l)
            return obj
        # range condition
        else:
            if lower < upper:
                obj = if_elif_else(type1, l, range_var, lower, upper, op1, op2)
                return obj
            if lower > upper:
                obj = if_elif_else(type1, l, range_var, upper, lower, lateral_op(op2), lateral_op(op1))
                return obj

    obj = if_elif_else(type1, l)
    return obj

