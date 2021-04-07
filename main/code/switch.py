import stack_match2

net_open = 0
dict_num_chain_pos = dict()
# for i1 in stack_match2.dict_num_list_of_chains:
#     dict_num_chain_pos[i1] = [0, 0]
z_new = []
dict_num_list_common_vars = dict()
seen_at_num = []
order = []  # need not actually be a list, can just be a var


def initialize_dict_num_chain_pos():
    global dict_num_chain_pos
    for i1 in stack_match2.dict_num_list_of_chains:
        dict_num_chain_pos[i1] = [0, 0]
        
        
def make_switch(z):
    global net_open
    global dict_num_chain_pos
    global z_new
    global dict_num_list_common_vars
    global seen_at_num
    global order

    initialize_dict_num_chain_pos()
    
    i = 0
    while i < len(z):
        print('in while', z[i], net_open, order)

        # check placement
        if seen_at_num and net_open < seen_at_num[-1]:
            seen_at_num.pop()

        if z[i] == '{':
            net_open += 1
            z_new.append(z[i])
            i += 1

        elif z[i] == '}':
            net_open -= 1
            z_new.append(z[i])

            if order and order[-1][1] == net_open:
                i = skip_extra_brackets(i + 1, z)
                order.pop()
            else:
                i += 1

        elif z[i] == 'if':
            if net_open not in seen_at_num:
                seen_at_num.append(net_open)
            else:
                dict_num_chain_pos[net_open][0] += 1
                dict_num_chain_pos[net_open][1] = 0

            beg_net_open_if = net_open

            chosen_var, range_lower_bound = check_change_to_switch(net_open)

            # chain to be switched
            # chosen var is the switch var
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[net_open]
                chain_pos = dict_num_chain_pos[net_open][0]
                if_obj = main_list[chain_pos][0]

                case_no, range_case = get_case_no(if_obj, chosen_var, range_lower_bound)
                z_new.append('switch(' + chosen_var + ') { case ' + case_no + ':')
                pre_body, new_pos = get_new_prebody(i, z, chosen_var, case_no, range_case)

                z_new.append(pre_body)
                i = new_pos

                order.append(('if', beg_net_open_if))

                dict_num_chain_pos[net_open][1] += 1  # incremented object by one

            # chain not switched
            else:
                print('chain not switched')
                z_new.append(z[i])
                i += 1

        elif z[i] == 'else':

            chosen_var, range_lower_bound = check_change_to_switch(seen_at_num[-1])

            # to be switched
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[seen_at_num[-1]]
                chain_pos = dict_num_chain_pos[seen_at_num[-1]][0]
                obj_no = dict_num_chain_pos[seen_at_num[-1]][1]
                chosen_chain = main_list[chain_pos]
                obj = chosen_chain[obj_no]
                if obj.type1 == 'elif':
                    dict_num_chain_pos[seen_at_num[-1]][1] += 1

                    net_open += 1

                    beg_net_open_elif = net_open

                    case_no, range_case = get_case_no(obj, chosen_var, range_lower_bound)
                    z_new.append('case ' + case_no + ':')
                    pre_body, new_pos = get_new_prebody(i + 4, z, chosen_var, case_no, range_case)

                    z_new.append(pre_body)
                    i = new_pos

                    order.append(('elif', beg_net_open_elif))

                else:
                    dict_num_chain_pos[seen_at_num[-1]][1] += 1

                    beg_net_open_else = net_open

                    z_new.append('default:')
                    i += 2

                    order.append(('else', beg_net_open_else))

            else:
                z_new.append(z[i])
                i += 1

        else:
            z_new.append(z[i])
            i += 1


# needs to include a way to check for || and other cases where switch should not be done
def check_change_to_switch(num):
    global dict_num_list_common_vars  # list of common variables for a chain
    global dict_num_chain_pos

    # switch based on first common var in all if elif else objects of a chain
    if num not in dict_num_list_common_vars.keys():
        dict_num_list_common_vars[num] = []
    elif num in dict_num_list_common_vars.keys():  # calculated for some chain at num earlier
        try:
            return dict_num_list_common_vars[num][dict_num_chain_pos[num][0]][
                       0], None  # calculated for same chain already

        # not calculated for chain
        except:
            print('error')

    try:
        # not calculated for chain
        dict_num_list_common_vars[num].append([])
        main_list = stack_match2.dict_num_list_of_chains[num]
        chain_pos = dict_num_chain_pos[num][0]
        l_chain = main_list[chain_pos].copy()  # l_chain is a chain

    except:
        return None, None

    # don't switch single if
    if len(l_chain) == 1:
        return None, None

    # else has no condition vars, so don't compare with that
    if l_chain[-1].type1 == 'else':
        l_chain.pop()

    count = 1
    rhs = set()
    if len(l_chain[0].condition_vars) > 0:
        i = l_chain[0].condition_vars[0]
        rhs.add(i[1])
        for j in l_chain[1:]:  # obj
            if len(j.condition_vars) == 0:
                return None, None

            k = j.condition_vars[0]  # tuple
            if k[0] == i[0]:
                if k[1] in rhs:
                    return None, None

                rhs.add(k[1])
                count += 1
        if count == len(l_chain):
            dict_num_list_common_vars[num][dict_num_chain_pos[num][0]].append(i[0])
            # print('returning', dict_num_list_common_vars[num][dict_num_chain_pos[num][0]][0])
            return dict_num_list_common_vars[num][dict_num_chain_pos[num][0]][0], None

    elif l_chain[0].range_var is not None:
        seq = [(l_chain[0].l, l_chain[0].u)]
        width = calculate_width(l_chain[0])
        for j in l_chain[1:]:
            if j.range_var is not None and j.range_var == l_chain[0].range_var:
                if l_chain[0].op1 == j.op1 and l_chain[0].op2 == j.op2 and width == calculate_width(j):
                    seq.append((j.l, j.u))
                else:
                    return None, None
            else:
                return None, None

        # seq.sort(key=lambda x: x[0])

        for i2 in range(1, len(seq)):
            if l_chain[0].op1 == '<=' and l_chain[0].op2 == '<=' and seq[i2][0] - 1 != seq[i2 - 1][1]:
                return None, None
            if l_chain[0].op1 == '<=' and l_chain[0].op2 == '<' and seq[i2][0] != seq[i2 - 1][1]:
                return None, None
            if l_chain[0].op1 == '<' and l_chain[0].op2 == '<=' and seq[i2][0] != seq[i2 - 1][1]:
                return None, None
            if l_chain[0].op1 == '<' and l_chain[0].op2 == '<' and seq[i2][0] != seq[i2 - 1][1] - 1:
                return None, None

        return switch_range_condition(l_chain[0]), l_chain[0].l

    return None, None


# def get_new_prebody(pos, z, var, cmp_with):
def get_new_prebody(pos, z, var, cmp_with, range_case):
    indices = [i for i, x in enumerate(z) if x == '{']  # list of positions of { in z
    end_here = -1
    # find first position of { after the curr pos
    for i in indices:
        if i > pos:
            end_here = i
            break

    if range_case:
        if z[pos] == 'if':
            return '', end_here
        for i in indices:
            if i > end_here:
                return '', i

    # look only from curr_pos + 1 till before a {
    z = z[pos + 1: end_here]
    indices = [i for i, x in enumerate(z) if x == var]  # list of positions of var in shortened z
    ret = ''
    for i in indices:
        if i + 2 < len(z) and z[i + 1] == '==' and z[i + 2] == cmp_with:
            # possible other condition before var
            if i - 1 >= 0 and z[i - 1] == '(':
                i_copy_l = i - 2
                while i_copy_l >= 0 and z[i_copy_l] == '(':
                    i_copy_l -= 1
                # first condition
                if i_copy_l < 0:
                    i_copy_r = i + 3
                    while i_copy_r < len(z) and z[i_copy_r] == ')':
                        i_copy_r += 1
                    # only condition
                    if i_copy_r == len(z):
                        return ret, end_here
                    # || after var==cmp_with in the beginning
                    elif z[i_copy_r] == '||':
                        return ret, end_here
                    # && after var==cmp_with in the beginning
                    elif z[i_copy_r] == '&&':
                        ret = 'if(' + ''.join(z[i_copy_r + 1:])
                        return ret, end_here
                    # other operator like > or < or == after var==cmp_with in the beginning
                    else:
                        ret = 'if(' + ''.join(z[i_copy_r + 1:])
                        return ret
                # not first condition
                elif i_copy_l >= 0:
                    ret = 'if'
                    return ret, pos + 1
            # not the first condition
            elif i - 1 >= 0 and z[i - 1] != '(':
                ret = 'if'
                return ret, pos + 1

        elif i - 2 >= 0 and z[i - 1] == '==' and z[i - 2] == cmp_with:
            # possible other condition before var
            if i - 3 >= 0 and z[i - 3] == '(':
                i_copy_l = i - 4
                while i_copy_l >= 0 and z[i_copy_l] == '(':
                    i_copy_l -= 1
                # first condition
                if i_copy_l < 0:
                    i_copy_r = i + 1
                    while i_copy_r < len(z) and z[i_copy_r] == ')':
                        i_copy_r += 1
                    # only condition
                    if i_copy_r == len(z):
                        return ret, end_here
                    # || after var==cmp_with in the beginning
                    elif z[i_copy_r] == '||':
                        return ret, end_here
                    # && after var==cmp_with in the beginning
                    elif z[i_copy_r] == '&&':
                        ret = 'if(' + ''.join(z[i_copy_r + 1:])
                        return ret, end_here
                    # other operator like > or < or == after var==cmp_with in the beginning
                    else:
                        ret = 'if(' + ''.join(z[i_copy_r + 1:])
                        return ret
                # not first condition
                elif i_copy_l >= 0:
                    ret = 'if'
                    return ret, pos + 1
            # not the first condition
            elif i - 3 >= 0 and z[i - 3] != '(':
                ret = 'if'
                return ret, pos + 1

    return ret, end_here


# actually it is to put break
def skip_extra_brackets(pos, z):
    global net_open
    global order
    global seen_at_num
    global z_new

    if order[-1][0] == 'else':
        z_new.append('break;}')

        while pos < len(z) and z[pos] == '}' and net_open != seen_at_num[-1]:
            net_open -= 1
            pos += 1
        return pos

    if order[-1][0] == 'if':
        z_new.append('break;')
        return pos

    if order[-1][0] == 'elif':
        if z[pos] == 'else':
            z_new.append('break;')
            return pos

        else:  # has to be a }
            z_new.append('break;}')
            while pos < len(z) and z[pos] == '}' and net_open != seen_at_num[-1]:
                net_open -= 1
                pos += 1
            return pos


def calculate_width(obj):
    if (obj.op1 == '<=' and obj.op2 == '<=') or (obj.op1 == '<' and obj.op2 == '<'):
        return obj.u - obj.l + 1
    if (obj.op1 == '<=' and obj.op2 == '<') or (obj.op1 == '<' and obj.op2 == '<='):
        return obj.u - obj.l


def switch_range_condition(obj):
    condition = ''
    if obj.op1 == '<=' and obj.op2 == '<=':
        w = obj.u - obj.l + 1
        condition += '(' + obj.range_var + '-(' + str(obj.l) + '))/' + str(w)
        return condition
    if obj.op1 == '<=' and obj.op2 == '<':
        w = obj.u - obj.l
        condition += '(' + obj.range_var + '-(' + str(obj.l) + '))/' + str(w)
        return condition
    if obj.op1 == '<' and obj.op2 == '<=':
        w = obj.u - obj.l
        condition += '(' + obj.range_var + '-(' + str(obj.l + 1) + '))/' + str(w)
        return condition
    if obj.op1 == '<' and obj.op2 == '<':
        # w = obj.u - obj.l + 1
        # condition += '(' + obj.range_var + '-(' + str(obj.l+1) + '))/' + str(w)

        w = obj.u - obj.l - 1  # (obj.u-1) - (obj.l+1) - 1
        condition += '(' + obj.range_var + '-(' + str(obj.l + 1) + '))/' + str(w)

        return condition


def get_case_no(obj, chosen_var, range_lower_bound):
    if obj.condition_vars != []:
        return list(filter(lambda x: chosen_var in x, obj.condition_vars))[0][1], False
    if obj.range_var is not None:
        if obj.op1 == '<=' and obj.op2 == '<=':
            return str((obj.l - range_lower_bound) / (obj.u - obj.l + 1)).split('.')[0], True
        if obj.op1 == '<=' and obj.op2 == '<':
            return str((obj.l - range_lower_bound) / (obj.u - obj.l)).split('.')[0], True
        if obj.op1 == '<' and obj.op2 == '<=':
            # return str((obj.l-(range_lower_bound+1))/(obj.u-obj.l)).split('.')[0], True

            return str((obj.l - range_lower_bound) / (obj.u - obj.l)).split('.')[0], True

        if obj.op1 == '<' and obj.op2 == '<':
            # return str((obj.l-(range_lower_bound+1))/(obj.u-obj.l+1)).split('.')[0], True

            return str((obj.l - range_lower_bound) / (obj.u - obj.l - 1)).split('.')[0], True
