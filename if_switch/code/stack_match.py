import re
from collections import deque


class if_elif_else:
    def __init__(self, type1, condition_vars):
        self.type = type1
        self.condition_vars = condition_vars
        self.len_condition_vars = len(self.condition_vars)


class chain:
    def __init__(self):
        self.same_list = []


dict_chain_obj = {}
dict_pos_for_chain_obj = {}


# --------------------------------------------------------------------------------------------------------

def create_obj(type1, pos, z, num):
    if type1 == 'if':
        i = pos + 2
        l = []
        while i < len(z) and z[i] != ')':
            if i + 2 < len(z) and i + 1 == '==':
                if (int(i) and re.match(r'^([\s\d]+)$', z[i + 2]) is None) or (
                        int(i + 2) and re.match(r'^([\s\d]+)$', z[i]) is None):
                    l.append((i, i + 2))
                    i += 3
            else:
                i += 1
        obj = if_elif_else('if', l)
        obj_chain = chain()
        obj_chain.same_list.append(obj)
        if dict_chain_obj[num]:
            dict_chain_obj[num].append(obj_chain)
        else:
            dict_chain_obj[num] = [obj_chain]
        dict_pos_for_chain_obj[num] = 0

    elif type1 == 'elif':
        i = pos + 2
        l = []
        while i < len(z) and z[i] != ')':
            if i + 2 < len(z) and i + 1 == '==':
                if (int(i) and re.match(r'^([\s\d]+)$', z[i + 2]) is None) or (
                        int(i + 2) and re.match(r'^([\s\d]+)$', z[i]) is None):
                    l.append((i, i + 2))
                    i += 3
            else:
                i += 1
        obj = if_elif_else('if', l)
        obj_chain = chain()
        obj_chain.same_list.append(obj)
        if dict_chain_obj[num]:
            dict_chain_obj[num].append(obj_chain)
        else:
            dict_chain_obj[num] = [obj_chain]
        obj = if_elif_else('elif', l)
        obj_chain = dict_chain_obj[num][dict_pos_for_chain_obj[num]]
        obj_chain.same_list.append(obj)

    elif type1 == 'else':
        obj = if_elif_else('else', None)
        dict_chain_obj[num][dict_pos_for_chain_obj[num]].same_list.append(obj)
        dict_pos_for_chain_obj[num] += 1


# --------------------------------------------------------------------------------------------------------

stack = deque()
temp_stack = deque()
net_open = 0
prev_else = -1
prev_if = -1
prev = -1


def make_chains(output_prg_pass1):
    global net_open
    global prev_else
    global prev_if
    global prev

    for i in range(len(output_prg_pass1)):
        if output_prg_pass1[i] == '{':
            net_open += 1

        elif output_prg_pass1[i] == '}':
            net_open -= 1

        elif output_prg_pass1[i] == 'if':
            prev_if = i
            if temp_stack:
                temp_stack.append((net_open, 'if'))
                if temp_stack[-1][-1] == 'if' and temp_stack[-2][-1] == 'else':
                    if temp_stack[-1][0] == temp_stack[-2][0] + 1:
                        temp_stack.pop()
                        temp_stack.pop()
                        create_obj('elif', i, output_prg_pass1, stack[-1][0])
                    elif temp_stack[-1][0] == temp_stack[-2][0]:
                        create_obj('else', prev_else, output_prg_pass1, stack[-1][0])
                        create_obj('if', i, output_prg_pass1, stack[-1][0])
                        temp_stack.popleft()
                        stack.pop()

            elif not stack:
                if net_open != stack[-1][0]:
                    prev += 1
                stack.append((net_open, 'if'))
                create_obj('if', i, output_prg_pass1, net_open)

            else:
                stack.append((net_open, 'if'))
                create_obj('if', i, output_prg_pass1, net_open)

        elif output_prg_pass1[i] == 'else':
            prev_else = i
            if stack[-1][0] == net_open and stack[-1][1] == 'if':
                stack.append((net_open, 'else'))
                temp_stack.append((net_open, 'else'))

            elif (prev > 0 and stack[prev][0] > net_open) or (prev == -1 and stack[-1][0] > net_open):
                if stack[-1][1] == 'else':
                    create_obj('else', i, output_prg_pass1, stack[-1][0])
                else:
                    while net_open != stack[-1][0]:
                        stack.pop()
                    prev -= 2
                    while temp_stack:
                        temp_stack.pop()
                if stack[-1][1] == 'if':
                    stack.append((net_open, 'else'))
                    temp_stack.append((net_open, 'else'))

        elif (prev > 0 and stack[prev][0] < net_open) or (prev == -1 and stack[-1][0] < net_open):
            temp_stack.append((net_open, 'else'))

        else:
            stack.pop()
            stack.pop()
            stack.append((net_open, 'else'))
            if len(stack) >= 2 and stack[-1][0] == stack[-2][0] and stack[-2][0] == 'if':
                temp_stack.append((net_open, 'else'))

    # --------------------------------------------------------------------------------------------------------

    if stack:
        if len(stack) == 1:
            if stack[-1][1] == 'if':
                create_obj('if', prev_if, output_prg_pass1, stack[-1][0])
            else:
                create_obj('else', prev_else, output_prg_pass1, stack[-1][0])

        elif len(stack) == 2:
            if stack[-1][0] != stack[-2][0]:
                create_obj('elif', prev_if, output_prg_pass1, stack[-2][0])
            else:
                if temp_stack and temp_stack[-1][1] == 'else':
                    create_obj('else', prev_else, output_prg_pass1, stack[-1][0])
                    temp_stack.pop()
                    stack.pop()
                    stack.pop()
