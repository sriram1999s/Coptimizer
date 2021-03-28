import stack_match2

net_open = 0
begin_net_open = 0
dict_num_chain_pos = stack_match2.dict_num_list_of_chains.fromkeys(stack_match2.dict_num_list_of_chains.keys(), [0, 0])
z_new = []


def make_switch(z):
    global net_open
    global dict_num_chain_pos
    global begin_net_open
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
            i += 1

        elif z[i] == 'if':
            begin_net_open = net_open
            dict_num_chain_pos[net_open][1] += 1  # incremented object by one
            chosen_var = check_change_to_switch(net_open)
            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[net_open]
                chain_pos = dict_num_chain_pos[net_open][0]
                if_obj = main_list[chain_pos][0]
                l = list(filter(lambda x: chosen_var in x, if_obj.condition_vars))
                z_new.append('switch(' + chosen_var + ') { case ' + l[0][1] + ':')
                pre_body, new_pos = get_new_prebody(i, z, chosen_var, l[0][1])
                z_new.append(pre_body)
                i = new_pos
            else:
                z_new.append(z[i])
                i += 1
            # dict_num_chain_pos[net_open][0] += 1

        elif z[i] == 'else':
            chosen_var = check_change_to_switch(begin_net_open)

            if chosen_var is not None:
                main_list = stack_match2.dict_num_list_of_chains[begin_net_open]
                chain_pos = dict_num_chain_pos[begin_net_open][0]
                obj_no = dict_num_chain_pos[begin_net_open][1]
                chosen_chain = main_list[chain_pos]
                obj = chosen_chain[obj_no]
                if obj.type1 == 'elif':
                    z_new.append('break;')
                    l = list(filter(lambda x: chosen_var in x, obj.condition_vars))
                    z_new.append('case ' + l[0][1] + ':')
                    pre_body, new_pos = get_new_prebody(i + 4, z, chosen_var, l[0][1])
                    z_new.append(pre_body)
                    i = new_pos

                else:
                    z_new.append('break;')
                    z_new.append('default:')
                    begin_net_open1 = net_open
                    i += 2
                    while i < len(z):
                        if z[i] == '{':
                            net_open += 1
                        elif z[i] == '}':
                            net_open -= 1
                        z_new.append(z[i])
                        if net_open == begin_net_open1:
                            break
                        i += 1
                    z_new.append('break;}')
                dict_num_chain_pos[begin_net_open][1] += 1

            else:
                z_new.append(z[i])
                i += 1

        else:
            z_new.append(z[i])
            i += 1


def check_change_to_switch(num):
    main_list = stack_match2.dict_num_list_of_chains[num]
    chain_pos = dict_num_chain_pos[num][0]
    l = main_list[chain_pos].copy()
    if len(l) == 1:
        return None
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
            return i[0]
        count = 1
    return None


def get_new_prebody(pos, z, var, cmp_with):
    global net_open
    global begin_net_open
    indices = [i for i, x in enumerate(z) if x == '{']
    end_here = -1
    for i in indices:
        if i > pos:
            end_here = i
            break

    z = z[pos + 1: end_here]
    # print('z', z, pos, end_here)
    indices = [i for i, x in enumerate(z) if x == var]
    ret = ''
    for i in indices:
        if i + 2 < len(z) and z[i + 1] == '==' and z[i + 2] == cmp_with:
            if i - 2 >= 0 and z[i - 1] == '(' and z[i - 2] == '!' and z[i + 3] == ')':
                ret += 'break;'
                # j = i + 3
                # while j < len(z):
                #     if z[j] == '{':
                #         net_open += 1
                #     elif z[i] == '}':
                #         net_open -= 1
                #     if net_open == begin_net_open:  # think of other logic to skip body
                #         return ret, j
                #     j += 1
                return ret, end_here
            elif i - 1 >= 0 and z[i - 1] == '&&':
                ret += 'if' + ''.join(z[:i - 1]) + ')'
            elif i - 1 >= 0 and z[i - 1] == '||':
                return ret, end_here

            if z[i - 1] == '(' and z[i + 3] == ')':  # condition is just var==cmp_with
                return ret, end_here

            if z[i + 3] == '&&':
                ret += 'if(' + ''.join(z[i + 4:])
            elif z[i + 3] == '||':
                return ret, end_here
    return ret, end_here

