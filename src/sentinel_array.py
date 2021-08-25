from parser_file import flatten
import re

class Arr:
    def __init__(self, name, no_of_dimesions, diemsions, no_of_positions_filled, type1):
        self.name = name
        self.no_of_dimensions = no_of_dimesions
        self.diemsions = diemsions
        self.alias = []
        self.filled = no_of_positions_filled
        self.type1 = type1

arr_obj_list = []

def initialize_arr_obj(init_statement, len1):
    global arr_obj_list
    no_of_dimensions = 0
    dimensions = []
    for i in init_statement[2]:
        if i=='[':
            no_of_dimensions+=1
        if i not in ['[', ']']:
            dimensions.append(i)
    if len1 == 5:
        obj = Arr(init_statement[1], no_of_dimensions, dimensions, 0, init_statement[0])
        arr_obj_list.append(obj)
    elif len1 == 7:
        init_list = list(flatten(init_statement[4]))
        filled = 0
        for i in init_list:
            if i not in ['{', '}', ',']:
                filled += 1
        obj = Arr(init_statement[1], no_of_dimensions, dimensions, filled, init_statement[0])
        arr_obj_list.append(obj)


def compare_and_set_alias(lhs, rhs):
    global arr_obj_list
    if type(rhs) == str:
        for i in arr_obj_list:
            if i.name == rhs or rhs in i.alias:
                i.alias.append(lhs)
                break
    elif type(rhs) == list:
        for i in rhs:
            if is_identifier(i):
                for j in arr_obj_list:
                    if j.name == i or i in j.alias:
                        j.alias.append(i)
                        return


def is_identifier(var):
    if re.search('^[A-Za-z_][A-Za-z0-9_]*', var):
        return True
    return False


def set_filled(comment):
    global arr_obj_list
    comment = comment.replace('/', '')
    comment = comment.replace('*', '')
    comment = comment.strip()
    if comment.startswith('filled'):
        arr_obj_list[-1].filled = int(comment[7: ])


def handle_sentinel(p, aim):
    aim = aim.replace('/', '')
    aim = aim.replace('*', '')
    aim = aim.strip()
    # print('aim', aim, p[0])
    if aim.startswith('sequential search') and p[0]=='while':
        # print('handle sequential search')
        body = list(flatten(p[2]))
        if_pos = body.index('if')
        if_body_beginning_pos = body.index('{', if_pos+1)
        if_cond = body[if_pos+1: if_body_beginning_pos]

        # print('arr name-'+aim[18:]+'-')
        swap_with_last, ele, filled = add_prebody_sentinel(aim[18:], if_cond)
        # print('prebody', swap_with_last)

        if_body_end_pos = body.index('}', if_body_beginning_pos+1)
        if_body = add_postbody_sentinel(aim[17:], p, if_body_beginning_pos, if_body_end_pos, ele, filled)
        # print('postbody', if_body)

        body = [str(i) for i in body]
        ret = swap_with_last + p[0] + '(!' + "".join(body[if_pos+1: if_body_beginning_pos]) + ')' + "".join(body[:if_pos]) + "".join(body[if_body_end_pos+1:]) + if_body
        return ret


def add_prebody_sentinel(arr_name, if_cond):
    global arr_obj_list
    equals_pos = if_cond.index('==')
    closing_paran_pos = if_cond.index(')', equals_pos+1)
    ele = None
    if closing_paran_pos-equals_pos == 2: # right
        ele = if_cond[equals_pos+1]
    else:   # left
        ele = if_cond[equals_pos-1]
    data_type = None
    filled = None
    for i in arr_obj_list:
        if arr_name == i.name:
            data_type = i.type1
            filled = i.filled
            break
    # print('prebody ret', data_type, arr_name, filled, ele)
    ret = data_type + ' temp= ' + arr_name + '[' + str(filled-1) + '];' + arr_name + '[' + str(filled-1) + ']=' + str(ele) + ';'
    return ret, ele, filled


def add_postbody_sentinel(arr_name, p, if_body_beginning_pos, if_body_end_pos, ele, filled):
    jump_pos = None
    body = list(flatten(p[2]))
    try:
        break_pos = body.index('break', if_body_beginning_pos, if_body_end_pos)
        try:
            return_pos = body.index('return', if_body_beginning_pos, if_body_end_pos)
            jump_pos = min(break_pos, return_pos)
        except ValueError:
            jump_pos = break_pos
    except ValueError:
        try:
            return_pos = body.index('return', if_body_beginning_pos, if_body_end_pos)
            jump_pos = return_pos
        except ValueError:
            print('Should not come here')
    semicolon_pos = body.index(';', jump_pos)

    ret = arr_name + '[' + str(filled-1) + ']=temp;' + 'if(' + arr_name + '[' + str(filled-1) + ']==' + str(ele) + '||i<' + str(filled) + ')' + "".join(body[if_body_beginning_pos: jump_pos]) + "".join(body[semicolon_pos+1:if_body_end_pos+1])
    return ret