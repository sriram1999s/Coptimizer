import stack_match2

net_open = 0
dict_num_chain_pos = dict()
z_new = []
dict_num_list_common_vars = dict()
seen_at_num = []
order = []  # need not actually be a list, can just be a var

class range_if_elif:
    def __init__(self, lb, start, end, op1, op2, u, if1=False, range_var='yes'):
        self.l = lb
        self.start = start
        self.end = end
        self.op1 = op1
        self.op2 = op2
        self.if1 = if1
        self.range_var = range_var
        self.u = u
d_range = dict()
range_j = -1


def initialize_dict_num_chain_pos():
    global dict_num_chain_pos
    for i1 in stack_match2.dict_num_list_of_chains:
        dict_num_chain_pos[i1] = [0, 0]


def make_switch(OPTIMIZE,z):
    if not OPTIMIZE:
        return
    global net_open
    global dict_num_chain_pos
    global z_new
    global dict_num_list_common_vars
    global seen_at_num
    global order

    global d_range
    global range_j

    initialize_dict_num_chain_pos()

    i = 0
    while i < len(z):
        # print('in while', z[i])

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
            # else:
            #     dict_num_chain_pos[net_open][0] += 1
            #     dict_num_chain_pos[net_open][1] = 0

            else:
                if not (i-1>=0 and z[i-1]=='else '):
                    # print('should not come here')
                    dict_num_chain_pos[net_open][0] += 1
                    dict_num_chain_pos[net_open][1] = 0

            chosen_var, range_lower_bound = check_change_to_switch(net_open)

            # chain to be switched
            # chosen var is the switch var
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[net_open]
                chain_pos = dict_num_chain_pos[net_open][0]
                if_obj = main_list[chain_pos][0]

                case_no, range_case = get_case_no(if_obj, chosen_var, range_lower_bound)

                if range_case:
                    range_obj = range_if_elif(range_lower_bound, len(z_new), -1, if_obj.op1, if_obj.op2, if_obj.u, True)
                    d_range[net_open] = [range_obj]
                    range_j = len(z_new)

                z_new.append('switch(' + chosen_var + ') { case ' + case_no + ':')
                pre_body, new_pos = get_new_prebody(i, z, chosen_var, case_no, range_case)

                z_new.append(pre_body)
                i = new_pos

                order.append(('if', net_open))

                dict_num_chain_pos[net_open][1] += 1  # incremented object by one

            # chain not switched
            else:
                # print('chain not switched')
                z_new.append(z[i])
                i += 1

        elif z[i] == 'else ':
            chosen_var, range_lower_bound = check_change_to_switch(net_open)

            # to be switched
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[net_open]
                chain_pos = dict_num_chain_pos[net_open][0]
                obj_no = dict_num_chain_pos[net_open][1]
                chosen_chain = main_list[chain_pos]
                obj = chosen_chain[obj_no]
                if obj.type1 == 'elif':
                    dict_num_chain_pos[net_open][1] += 1

                    case_no, range_case = get_case_no(obj, chosen_var, range_lower_bound)

                    if range_case:
                        range_obj = range_if_elif(obj.l, len(z_new), -1, obj.op1, obj.op2, obj.u)
                        d_range[net_open].append(range_obj)

                    z_new.append('case ' + case_no + ':')
                    pre_body, new_pos = get_new_prebody(i + 1, z, chosen_var, case_no, range_case)

                    z_new.append(pre_body)
                    i = new_pos

                    order.append(('elif', net_open))

                else:
                    dict_num_chain_pos[net_open][1] += 1

                    z_new.append('default:')
                    i += 1

                    order.append(('else', net_open))

            else:
                print('else not switched')
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
            # print('error')
            None

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

        seq.sort(key=lambda x: x[0])

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
    z = z[pos + 2: end_here]
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
                        return ret  # add other value to return
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
                        return ret  # add other value to return
                # not first condition
                elif i_copy_l >= 0:
                    ret = 'if'
                    return ret, pos + 1
            # not the first condition
            elif i - 3 >= 0 and z[i - 3] != '(':
                ret = 'if'
                return ret, pos + 1

    return ret, end_here


def skip_extra_brackets(pos, z):
    global order
    global z_new

    global net_open
    global d_range

    if order[-1][0] == 'else':
        z_new.append('break;}')

        if net_open in d_range.keys():
            d_range[net_open][-1].end = len(z_new)
            reorder()

        return pos

    if order[-1][0] == 'if':
        z_new.append('break;')

        if net_open in d_range.keys():
            d_range[net_open][-1].end = len(z_new)

        return pos

    if order[-1][0] == 'elif':
        if z[pos] == 'else ':
            z_new.append('break;')

            if net_open in d_range.keys():
                d_range[net_open][-1].end = len(z_new)

            return pos

        else:  # has to be a }
            z_new.append('break;}')

            if net_open in d_range.keys():
                d_range[net_open][-1].end = len(z_new)
                reorder()

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
    # if obj.condition_vars != []:

    if obj.range_var is None:

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


def reorder():
    global net_open
    global d_range
    global z_new
    global range_j

    # print('z new begin', z_new)
    min1 = -1
    z_copy = []

    beg = range_j

    # get lower bound of chain
    for i in d_range[net_open]:
        if min1 == -1:
            min1 = i.l
        else:
            min1 = min(min1, i.l)

    # sort chain by starting pos
    # d = dict()
    # for k in d_range:
    #     d[k] = sorted(d_range[k], key=lambda x: x.start)

    # sort chain by lower bound
    d1 = dict()
    for k in d_range:
        d1[k] = sorted(d_range[k], key=lambda x: x.l)

    for i1 in d_range.keys():
        # not part of this chain
        if i1<net_open:
            continue

        # add switch condition
        for ob in d_range[i1]:
            if ob.if1:
                minus = z_new[range_j].find('-')
                indices = [i for i, x in enumerate(z_new[range_j]) if x == ')']  # list of positions of ) in z_new
                for k in indices:
                    if k > minus:
                        case = z_new[range_j].find('case ')
                        after = z_new[range_j][k:case]
                        break
                # replacing lower bound in switch
                z_copy.append(z_new[range_j][:minus + 2] + str(min1) + after)
                break

        while d1[i1]:
            # add case
            new_case_no, bool_range = get_case_no(d1[i1][0], 'does not matter', min1)
            z_copy.append('case ' + str(new_case_no) + ':')

            # add body
            for body_ele in z_new[d1[i1][0].start + 1:d1[i1][0].end]:
                z_copy.append(body_ele)
            d1[i1].pop(0)

            if d1[i1] and d1[i1][0].if1:
                range_j = d1[i1][0].start
            else:
                if d1[i1] != []:
                    range_j = d1[i1][0].start
                if z_copy[-1] == 'break;}':
                    z_copy[-1] = 'break;'
            # print('z copy else', z_copy)

    z_copy[-1] = 'break;}'

    z_new[beg:] = z_copy

    d_range.pop(net_open)
    # range_j = len(z_new)
    print('returning', z_new)
    print()






