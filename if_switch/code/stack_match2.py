class if_elif_else:
    def __init__(self, type1, condition_vars):
        self.type1 = type1
        self.condition_vars = condition_vars


dict_num_list_of_chains = dict()


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_char(s):
    if len(s) == 1 and s.isalpha():
        return True
    else:
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
        i = pos + 2
        l = []
        while i < len(z) and z[i] != ')':
            if i + 2 < len(z) and z[i + 1] == '==':
                if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i+2]):
                    # if before or after are || don't add var to list because should not switch
                    if z[i-1] != '||' and z[i+3] != '||':
                        if z[i-2] != '!':
                            l.append((z[i+2], z[i]))
                elif (is_int(z[i+2]) or is_char(z[i+2])) and not is_int(z[i]):
                    # if before or after are || don't add var to list because should not switch
                    if z[i-1] != '||' and z[i+3] != '||':
                        if z[i - 2] != '!':
                            l.append((z[i], z[i + 2]))
                i += 3
            else:
                i += 1
        obj = if_elif_else('if', l)
        return obj

    if type1 == 'elif':
        i = pos + 2
        l = []
        while i < len(z) and z[i] != ')':
            if i + 2 < len(z) and z[i + 1] == '==':
                if (is_int(z[i]) or is_char(z[i])) and not is_int(z[i+2]):
                    l.append((z[i + 2], z[i]))
                elif (is_int(z[i+2]) or is_char(z[i+2])) and not is_int(z[i]):
                    l.append((z[i], z[i + 2]))
                i += 3
            else:
                i += 1
        obj = if_elif_else('elif', l)
        return obj

    if type1 == 'else':
        obj = if_elif_else('else', None)
        return obj


def find_prev_num(num):
    global dict_num_list_of_chains
    ret = -1
    for i in dict_num_list_of_chains.keys():
        if i < num:
            ret = i
        elif i==num:
            ret = i
            break
        else:
            break
    print('ret', ret)
    return ret