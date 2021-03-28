import stack_match2

net_open = 0
begin_net_open = 0
dict_num_chain_pos = stack_match2.dict_num_list_of_chains.fromkeys(stack_match2.dict_num_list_of_chains.keys(), [0, 0])
z_new = []
dict_num_list_common_vars = dict()
seen_at_num = []


def make_switch(z):
    global net_open
    global dict_num_chain_pos
    global begin_net_open
    global z_new
    global dict_num_list_common_vars
    global seen_at_num

    i = 0
    while i < len(z):
        print('in while', z[i], z_new)

        if z[i] == '{':
            net_open += 1
            z_new.append(z[i])
            i += 1

        elif z[i] == '}':
            net_open -= 1
            z_new.append(z[i])
            i += 1

        elif z[i] == 'if':
            if net_open not in seen_at_num:
                seen_at_num.append(net_open)
            else:
                dict_num_chain_pos[net_open][0] += 1
                dict_num_chain_pos[net_open][1] = 0

            begin_net_open = net_open

            # print('obj type', dict_num_chain_pos[net_open][1], stack_match2.dict_num_list_of_chains[net_open][dict_num_chain_pos[net_open][0]])
            chosen_var = check_change_to_switch(net_open)

            # chain to be switched
            # chosen var is the switch var
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[net_open]
                chain_pos = dict_num_chain_pos[net_open][0]
                if_obj = main_list[chain_pos][0]

                # list of tuples with chosen var
                l = list(filter(lambda x: chosen_var in x, if_obj.condition_vars))

                # by default choose the first tuple and get cmp_with value at index pos 1 of tuple
                z_new.append('switch(' + chosen_var + ') { case ' + l[0][1] + ':')

                # get how to deal with condition and where to read z from after handling that
                pre_body, new_pos = get_new_prebody(i, z, chosen_var, l[0][1])

                z_new.append(pre_body)
                i = util(new_pos, z, begin_net_open)

                dict_num_chain_pos[net_open][1] += 1  # incremented object by one


            # chain not switched
            else:
                z_new.append(z[i])
                i += 1

        elif z[i] == 'else':
            chosen_var = check_change_to_switch(begin_net_open)

            # to be switched
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[begin_net_open]
                chain_pos = dict_num_chain_pos[begin_net_open][0]
                obj_no = dict_num_chain_pos[begin_net_open][1]
                # print('obj no', obj_no)
                chosen_chain = main_list[chain_pos]
                obj = chosen_chain[obj_no]
                if obj.type1 == 'elif':
                    dict_num_chain_pos[begin_net_open][1] += 1

                    l = list(filter(lambda x: chosen_var in x, obj.condition_vars))
                    z_new.append('case ' + l[0][1] + ':')
                    pre_body, new_pos = get_new_prebody(i + 4, z, chosen_var, l[0][1])
                    z_new.append(pre_body)
                    i = util(new_pos, z, net_open)

                else:
                    dict_num_chain_pos[begin_net_open][1] += 1

                    z_new.append('default:')
                    i += 2
                    i = util(i, z, net_open)

            else:
                z_new.append(z[i])
                i += 1

        else:
            z_new.append(z[i])
            i += 1


# needs to include a way to check for || and other cases where switch should not be done
def check_change_to_switch(num):
    global dict_num_list_common_vars  # list of common variables for a chain
    # print('dict num list common vars')
    # for i in dict_num_list_common_vars:
    #     print(i, ':')
    #     for j in dict_num_list_common_vars[i]:  # list of list of tuples
    #         for k in j:
    #             print(k, ', ', end='')
    #         print()

    # switch based on first common var in all if elif else objects of a chain
    if num not in dict_num_list_common_vars.keys():
        dict_num_list_common_vars[num] = []

    elif num in dict_num_list_common_vars.keys():   # calculated for some chain at num earlier
        try:
            return dict_num_list_common_vars[num][dict_num_chain_pos[num][0]][0]    # calculated for same chain already
        # not calculated for chain
        except IndexError:
            # dict_num_list_common_vars[num].append([])
            print('index error')

    # not calculated for chain
    dict_num_list_common_vars[num].append([])
    main_list = stack_match2.dict_num_list_of_chains[num]
    chain_pos = dict_num_chain_pos[num][0]
    l = main_list[chain_pos].copy()  # l is a chain

    # don't switch single if
    if len(l) == 1:
        return None
    # else has no condition vars, so don't compare with that
    if l[-1].type1 == 'else':
        l.pop()

    count = 1
    for i in l[0].condition_vars:  # tuple
        for j in l[1:]:  # obj
            for k in j.condition_vars:  # tuple
                if k[0] == i[0]:
                    count += 1
                    break
        if count == len(l):
            dict_num_list_common_vars[num][dict_num_chain_pos[num][0]].append(i[0])
            return dict_num_list_common_vars[num][dict_num_chain_pos[num][0]][0]
        count = 1
    return None


def get_new_prebody(pos, z, var, cmp_with):
    global net_open
    global begin_net_open
    indices = [i for i, x in enumerate(z) if x == '{']  # list of positions of { in z
    end_here = -1
    # find first position of { after the curr pos
    for i in indices:
        if i > pos:
            end_here = i
            break

    # look only from curr_pos + 1 till before a {
    z = z[pos + 1: end_here]
    indices = [i for i, x in enumerate(z) if x == var]  # list of positions of var in shortened z
    ret = ''
    for i in indices:
        if i + 2 < len(z) and z[i + 1] == '==' and z[i + 2] == cmp_with:
            if i - 1 >= 0 and z[i - 1] == '&&':  # && before var
                ret += 'if' + ''.join(z[:i - 1]) + ')'

            if i - 1 >= 0 and z[i - 1] == '(' and z[i + 3] == ')':  # condition is just var==cmp_with
                return ret, end_here

            if z[i + 3] == '&&':  # && after var
                ret += 'if(' + ''.join(z[i + 4:])
    return ret, end_here


def skip_extra_brackets(pos, z):
    global begin_net_open
    i = pos
    while i < len(z) and z[i] == '}':
        i += 1

    if i < len(z):
        if z[i] == 'else':
            z_new.append('break;')
            return i
        z_new.append('break;}')
        return i

    z_new.append('break;}')
    for j in range(begin_net_open):
        z_new.append('}')
    return i


def util(pos, z, begin_net_open1):
    global net_open
    i = pos
    while i < len(z):
        if z[i] == '{':
            net_open += 1
        elif z[i] == '}':
            net_open -= 1
        # append no matter which character
        z_new.append(z[i])
        if net_open == begin_net_open1:
            i += 1
            break
        i += 1

    i = skip_extra_brackets(i, z)
    return i
