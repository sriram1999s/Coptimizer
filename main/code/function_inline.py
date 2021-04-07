import copy
from collections.abc import Iterable

fn_defn_list = []  # list of tuple of fn_defn having parsed list and "defn"
fn_defn_obj_list = []  # list of objects having function definition details

fn_call_list = []  # list of tuple of fn_call having parsed list and "call"
fn_call_obj_list = []  # list of objects having function call details

# new
def check_inline(l1, start, length, fn_name,l2):
    if start >= length:
        return
    elif l1[start] == fn_name:
        l2[0] = 0
        return
    elif (type(l1[start]) is tuple) or (type(l1[start]) is list):
        check_inline(l1[start],0,len(l1[start]),fn_name,l2)

    check_inline(l1, start + 1, length, fn_name,l2)

def inline_defn_helper(parsed_list,fn_name):
    l3 = [1]
    check_inline(parsed_list[5][0], 0, len(parsed_list[5][0]), parsed_list[1], l3)
    in_flag = l3[0];
    if(in_flag == 1):
        parsed_list1 = copy.deepcopy(parsed_list)
        fn_defn_list.append((fn_name,parsed_list1, "definition"));
        create_defn_obj(parsed_list1,in_flag);
    else:
        fn_defn_list.append((fn_name,parsed_list, "definition"));
        create_defn_obj(parsed_list,in_flag);

    return (fn_name,parsed_list,'definition')

def check_return(l1, start, length,l2):
    if start >= length:
        return
    elif l1[start] == 'return':
        l2[0] += 1
    elif (type(l1[start]) is list) or (type(l1[start]) is tuple):
        check_return(l1[start],0,len(l1[start]),l2)

    return check_return(l1, start + 1, length,l2)

def change_to_string(l1):
    ret_list = []
    if len(l1) > 1:
        if(type(l1[0]) is list):
            i = 0
            str_temp = ""
            while i < len(l1[0]):
                if(l1[0][i] == ','):
                    ret_list.append(str_temp.strip())
                    str_temp = ""
                    i += 1;
                    continue;
                str_temp += l1[0][i] + ' '
                i += 1;
            str_temp = ' '.join(l1[1])
            ret_list.append(str_temp)
        else:
            str_temp = ' '.join(l1)
            ret_list.append(str_temp)
    elif len(l1) == 1:
        str_temp = l1[0][0] + ' ' + l1[0][1]
        ret_list.append(str_temp)

    return ret_list

def create_defn_obj(parsed_list, inline_flag1):

    # l3 = [1]
    # check_inline(parsed_list[5][0], 0, len(parsed_list[5][0]), parsed_list[1], l3)
    # inline_flag = l3[0]

    inline_flag = inline_flag1;

    l2 = [0]
    check_return(parsed_list[5][0], 0, len(parsed_list[5][0]),l2)
    if(l2[0] == 0):
        return_id_or_val = None
    else:
        return_id_or_val = 1;
    str_params_list = change_to_string(parsed_list[3])

    obj = fn_defn_class(parsed_list[1], str_params_list, parsed_list[5], inline_flag, return_id_or_val, str(parsed_list[0]))
    fn_defn_obj_list.append(obj)

def call_helper(parsed_list,fn_name):
    length = len(parsed_list)
    if(length == 6):
        if(parsed_list[0] == 'return'):
            l1 = copy.deepcopy(parsed_list)
            fn_call_list.append((fn_name , l1[1:] , "call" , "ret" , "ret" , "return"))
            create_call_obj(l1[1:] , fn_name)
        else :
            l1 = copy.deepcopy(parsed_list[2:])
            fn_call_list.append((fn_name , l1 , "call" , parsed_list[0]))
            create_call_obj(l1,fn_name)

    elif(length == 8):
        l1 = copy.deepcopy(parsed_list[3:])
        fn_call_list.append((fn_name , l1 , "call" , parsed_list[0] , parsed_list[1]))
        create_call_obj(l1,fn_name)

    elif(length == 5):
        l1 = copy.deepcopy(parsed_list[0 : -1])
        fn_call_list.append((fn_name,l1, "call"))
        create_call_obj(l1,fn_name)
    #print("fn_call_list : ", fn_call_list)

# def get_arg_expr(i,n,arg_list,arg):
#     if(i == n):
#         return
#     elif(type(arg_list[i]) is list):
#         get_arg_expr(0,len(arg_list[i]),arg_list[i],arg)
#     elif(type(arg_list[i]) is str):
#         arg[0] = arg[0] + arg_list[i]
#     get_arg_expr(i+1,n,arg_list,arg)


def create_call_obj(parsed_list,fn_name):
    temp = []
    if(type(parsed_list[2]) is list):
        temp1 = list(flatten(parsed_list[2]))
        str_temp = ""
        for i in temp1:
            if(i == ','):
                temp.append(str_temp.strip())
                str_temp = ""
                continue
            str_temp += str(i) + ' '
        if(str_temp != ""):
            temp.append(str_temp.strip())
    else:
        temp.append(str(parsed_list[2]))

    obj1 = fn_call_class(fn_name, temp)
    fn_call_obj_list.append(obj1)

class fn_defn_class:
    def __init__(self, name, param_list, body, inline_flag, return_id_or_val, return_type):
        self.name = name
        self.param_list = param_list
        self.body = body
        self.inline_flag = inline_flag  # 0 => don't inline, 1 => inline
        self.return_id_or_val = None
        if return_id_or_val is not None:
            self.return_id_or_val = 1
        # self.return_id_or_val = return_id_or_val
        self.return_type = return_type


class fn_call_class:
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

# g33/((g22+g33)*g22)
# ------------functions from my_detector --------#

def get_defn_t_ix(fn_name):
    for ix in range(len(fn_defn_list)):
        if(fn_defn_list[ix][0] == fn_name):
            return ix
    return None

def remove_nested_calls(i,n,z):
    if(i == n):
        return;
    elif(type(z[i]) is list):
        remove_nested_calls(0,len(z[i]),z[i])
    elif(type(z[i]) is tuple):
        l = copy.deepcopy(z[i][1])
        z.insert(i,l)
        z.pop(i+1)
        remove_nested_calls(0,len(z[i]),z[i])

    remove_nested_calls(i + 1,len(z),z)

def remove_return(i,n,fn_body, hash_val):
    if(i == n):
        return
    elif(type(fn_body[i]) is list):
        remove_return(0,len(fn_body[i]),fn_body[i],hash_val)
    elif(type(fn_body[i]) is tuple):
        if(len(fn_body[i]) == 6 and fn_body[i][-1] == "return"):
            t = fn_body[i]
            t = list(t)
            t[-1] = "temp_" + hash_val + " = "
            t = tuple(t)
            call_t_ix1 = fn_call_list.index(fn_body[i])
            t1 = fn_call_list[call_t_ix1]
            t1 = list(t1)
            t1[-1] = "temp_" + hash_val + " = "
            t1 = tuple(t1)
            fn_call_list.insert(call_t_ix1,t1)
            temp_obj = copy.deepcopy(fn_call_obj_list[call_t_ix1])
            fn_call_obj_list.insert(call_t_ix1,temp_obj)
            fn_body.insert(i,t)
            fn_body.pop(i + 1)
        else :
            remove_return(0,len(fn_body[i]),fn_body[i],hash_val)
    elif(type(fn_body[i]) is str and fn_body[i] == "return"):
        fn_body[i] = "temp_" + hash_val + " = "

    remove_return(i+1,len(fn_body),fn_body, hash_val)

def remove_return1(i,n,fn_body, hash_val,goto_flag):
    if(i == n):
        return
    elif(type(fn_body[i]) is list):
        remove_return1(0,len(fn_body[i]),fn_body[i], hash_val,goto_flag)
    elif(fn_body[i] == "return"):
        fn_body[i] = " goto label_" + hash_val
        goto_flag[0] = 1

    remove_return1(i+1,len(fn_body),fn_body,hash_val,goto_flag)

def add_param_hash(hash_val,parameter_list1):
    length = len(parameter_list1)
    for ix in range(length):
        parameter_list1[ix] += "_" + hash_val

def get_param_vars(parameter_list1):
    var_list = []
    length = len(parameter_list1)
    for ix in range(length):
        var = parameter_list1[ix].split(" ")[-1]
        var_list.append(var)

    return var_list

def replace_param(i,n,fn_body,parameter_list2,hash_val):
    if(i == n):
        return
    elif(type(fn_body[i]) is list):
        replace_param(0 , len(fn_body[i]) , fn_body[i] , parameter_list2 , hash_val)
    elif(fn_body[i] in parameter_list2):
        fn_body[i] += "_" + hash_val

    replace_param(i+1,n,fn_body,parameter_list2,hash_val)

def retrieve_defn(i,n,fn_body):
    if(i == n):
        return
    elif(type(fn_body[i]) is list):
        retrieve_defn(0,len(fn_body[i]),fn_body[i])
    elif(type(fn_body[i]) is tuple):
        fn_call1 = []
        if(len(fn_body[i]) == 5):
            ret_dec = " " + fn_body[i][3] + " " + fn_body[i][4] + " = "
            fn_call1.append(ret_dec)
            fn_call1.append(fn_body[i][1])
            #fn_call1.append(';')
        elif(len(fn_body[i]) == 4):
            ret_dec = " " + fn_body[i][3] + " = "
            fn_call1.append(ret_dec)
            fn_call1.append(fn_body[i][1])
            #fn_call1.append(';')
        elif(len(fn_body[i]) == 6):
            if(fn_body[i][-1] == "return"):
                fn_call1 = fn_body[i][1]
                fn_call1.insert(0," return ")
            else :
                fn_call1 = fn_body[i][1]
                fn_call1.insert(0," " + fn_body[i][-1] + " ")
        else:
            fn_call1 = fn_body[i][1]

        fn_body.insert(i,fn_call1)
        fn_body.pop(i + 1)

    retrieve_defn(i+1,len(fn_body),fn_body)
