''' details of every if, else if, and else condition
type1 - indicates whether the object represents an if condition, else if condition, or else case
condition_vars - the list of variables used in the conditional statements
range_var - if the variable used in the condition is being checked for being part of uniform, unbroken ranges
l - lower bound of range cases
u - upper bound of range cases
op1 - the operator between range_var and the lower bound (<, <=, >, >=)
op2 - the operator between range_var and the upper bound (<, <=, >, >=)
'''
class if_elif_else:
    def __init__(self, type1, condition_vars, range_var=None, l=None, u=None, op1=None, op2=None):
        self.type1 = type1
        self.condition_vars = condition_vars

        self.l = l
        self.u = u
        self.op1 = op1
        self.op2 = op2
        self.range_var = range_var

        
''' key: the number of open braces when the chain starts, it denotes the nesting level of the chain
value: list of chains of if_elif_else objects '''
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
    # print('s', s)
    if s[0] == "'" and s[-1] == "'":
        return True
    return False


''' identify matching if, else if, and else conditions and store each such chain in a common list '''
def identify_chains(OPTIMIZE, z):
    if (not OPTIMIZE):
        return
    global dict_num_list_of_chains
    net_open = 0

    ''' Go through the parse tree element by element while maintaining the number of open braces in the variable net_open. 
    This variable helps to identify if, else if, and else which are associated with each other. 
    For an 'if' condition, create an object with all the its condition details. If it is the first 'if' at that level of nesting, create a new key in the global dictionary with value as a list containing the object. If is not the first 'if' at that level of nesting, a new key need not be created and the new list with this object can be appended to the existing key. 
    For an 'else if' or 'else' condition, create an object with all the its condition details and append this object to the list containing the corresponding 'if' condition object. 
    '''
    i = 0
    while i < len(z):

        if z[i] == '{':
            net_open += 1
            i += 1

        elif z[i] == '}':
            net_open -= 1
            i += 1

        elif z[i] == 'if':
            obj = create_obj('if', i, z)
            if net_open not in dict_num_list_of_chains.keys():
                dict_num_list_of_chains[net_open] = [[obj]]
            else:
                dict_num_list_of_chains[net_open].append([obj])
            i += 1

        elif z[i] == 'else':
            if i+2 < len(z) and z[i+1] == ' ' and z[i+2] == 'if':
                obj = create_obj('elif', i+2, z)
                i+=3
            else:
                obj = create_obj('else', i, z)
                i += 1
            dict_num_list_of_chains[net_open][-1].append(obj)


        else:
            i += 1


def create_obj(type1, pos, z):
    if type1 == 'if':
        return util('if', z, pos + 2)

    if type1 == 'elif':
        return util('elif', z, pos + 2)

    if type1 == 'else':
        obj = if_elif_else('else', None)
        return obj


''' helper function '''
def skip_while(pos, ch, z):
    while pos < len(z) and z[pos] == ch:
        pos += 1
    return pos


''' helper function that helps to store the operators in a uniform manner in the object '''
def lateral_op(op):
    if op == '<':
        return '>'
    if op == '>':
        return '<'
    if op == '<=':
        return '>='
    if op == '>=':
        return '<='


''' check whether the condition is of the type that can be switched, or if it compares a variable with a uniform, unbroken range. Create and return an object accordingly ''' 
def util(type1, z, i):
    l1 = []
    range_ops = ['<=', '>=', '<', '>']
    i = skip_while(i, '(', z)
    if i + 2 < len(z) and z[i + 1] == '==':
        if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i + 2]):
             # if after is || don't add var to list because should not switch 
            if z[i + 3] != '||':
                l1.append((z[i + 2], z[i]))
        elif (is_int(z[i + 2]) or is_char(z[i + 2])) and not is_int(z[i]):
            # if after is || don't add var to list because should not switch
            if z[i + 3] != '||':
                l1.append((z[i], z[i + 2]))

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
            obj = if_elif_else(type1, l1)
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
            obj = if_elif_else(type1, l1)
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
            obj = if_elif_else(type1, l1)
            return obj

        i = skip_while(i + 1, ')', z)

        # other operator
        if z[i] != '&&':
            obj = if_elif_else(type1, l1)
            return obj

        i = skip_while(i + 1, '(', z)

        # const
        if is_int(z[i]):
            upper = int(z[i])
        # var
        elif not is_int(z[i]):
            if z[i] != range_var:
                obj = if_elif_else(type1, l1)
                return obj
        # other
        else:
            obj = if_elif_else(type1, l1)
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
            obj = if_elif_else(type1, l1)
            return obj

        i = skip_while(i + 1, ')', z)

        # const is seen for the first time
        if is_int(z[i]) and upper is None:
            upper = int(z[i])

        # var is seen for the first time
        elif not is_int(z[i]):
            if range_var != z[i]:
                obj = if_elif_else(type1, l1)
                return obj
            else:
                pass
        # other
        else:
            obj = if_elif_else(type1, l1)
            return obj

        i = skip_while(i + 1, ')', z)

        # more conditions
        if z[i] != '{':
            obj = if_elif_else(type1, l1)
            return obj
        # range condition
        else:
            if lower < upper:
                obj = if_elif_else(type1, l1, range_var, lower, upper, op1, op2)
                return obj
            if lower > upper:
                obj = if_elif_else(type1, l1, range_var, upper, lower, lateral_op(op2), lateral_op(op1))
                return obj

    obj = if_elif_else(type1, l1)
    return obj
