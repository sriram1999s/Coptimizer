def dummy_fn():
    print("YO")

fn_defn_obj_dict = dict()
fn_call_obj_dict = dict()


class fn_defn_class:
    def __init__(self, ret_type, fn_name, formal_parameters, body):
        self.ret_type = ret_type
        self.fn_name = fn_name
        self.formal_parameters = change_to_string(formal_parameters)
        self.body = body
        self.inline_flag = body is not None and check_inline(self.body[0], 0, len(self.body[0]), self.fn_name)
        self.return_id_or_val = check_return(self.body[0], 0, len(self.body[0]))


class fn_call_class:
    def __init__(self, fn_name, actual_arguments, return_into):
        self.fn_name = fn_name
        self.actual_arguments = process_args(actual_arguments)
        self.return_into = return_into


def process_args(p):
    processed = []
    if type(p) is list:
        for i in p:
            if i !=',':
                processed.append(str(i))
    return processed


def check_inline(l1, start, length, fn_name):
    # print('l1', l1)
    if start >= length:
        return 1
    if type(l1[start]) == str and l1[start] == fn_name:
        return 0
    elif type(l1[start]) == list:
        for i in l1[start]:
            if type(i) == list and check_inline(i, 0, len(i), fn_name) == 0:
                return 0
    start += 1
    return check_inline(l1, start, length, fn_name)

def check_return(l1, start, length):
    if start >= length:
        return None
    if type(l1[start]) == str and l1[start] == 'return':
        return l1[start + 1]
    elif type(l1[start]) == list:
        for i in l1[start]:
            if type(i) == list:
                ret = check_return(i, 0, len(i))
                if ret:
                    return str(ret)
    start += 1
    return check_return(l1, start, length)

def change_to_string(l1):
    ret_list = []
    if len(l1) > 1:
        i = 0
        while i < len(l1[0]):
            str_temp = l1[0][i] + ' ' + l1[0][i + 1]
            i += 3
            ret_list.append(str_temp)
        ret_list.append(l1[1][0] + ' ' + l1[1][1])
    elif len(l1) == 1:
        str_temp = l1[0][0] + ' ' + l1[0][1]
        ret_list.append(str_temp)

    return ret_list

def create_defn_obj(ret_type, fn_name, formal_parameters, body):
    if fn_name not in fn_defn_obj_dict:
        if body == ';': # prototype
            body = None
        obj = fn_defn_class(ret_type, fn_name, formal_parameters, body)
        fn_defn_obj_dict[fn_name] = obj
    else:
        fn_defn_obj_dict[fn_name].formal_parameters = formal_parameters
        fn_defn_obj_dict[fn_name].body = body
        fn_defn_obj_dict[fn_name].inline_flag = check_inline(body, 0, len(body), fn_name)


def create_call_obj(fn_name, actual_arguments, return_into):
    if fn_name not in fn_call_obj_dict:
        fn_call_obj_dict[fn_name] = []
    obj = fn_call_class(fn_name, actual_arguments, return_into)
    fn_call_obj_dict[fn_name].append(obj)


def inline(from_func, fn_name, actual_args, ret_into):
    send = []
    print('from func', from_func, actual_args)
    if from_func == 'p_function_call':
        size = len(fn_defn_obj_dict[fn_name].formal_parameters)
        s = []
        for i in range(size):
            s.append(fn_defn_obj_dict[fn_name].formal_parameters[i] + "=" + str(actual_args[i]) + ";")
        send.append(s)
        flattened = list(flatten(fn_defn_obj_dict[fn_name].body))
        s = []
        i = 0
        while i < len(flattened):
            if flattened[i] != 'return':
                s.append(flattened[i])
                i+=1
            elif flattened[i]=='return' and i+1<len(flattened) and flattened[i+1]!=';':
                s_str = str(fn_defn_obj_dict[fn_name].ret_type) + ' temp=' + str(flattened[i+1])
                if i+2>=len(flattened):
                    s_str+=';'
                s.append(s_str)
                i+=2
        send.append(s)

    elif from_func == 'p_expr':
        size = len(fn_defn_obj_dict[fn_name].formal_parameters)
        s = []
        for i in range(size):
            s.append(fn_defn_obj_dict[fn_name].formal_parameters[i] + "=" + str(actual_args[i]) + ";")
        send.append(s)
        flattened = list(flatten(fn_defn_obj_dict[fn_name].body))
        s = []
        i = 0
        while i < len(flattened):
            if flattened[i] != 'return':
                s.append(flattened[i])
                i += 1
            elif flattened[i] == 'return' and i + 1 < len(flattened) and flattened[i + 1] != ';':
                s_str = str(ret_into) + "=" + str(flattened[i])
                if i + 2 >= len(flattened):
                    s_str += ';'
                s.append(s_str)
                i += 2
        send.append(s)
    return send

from collections.abc import Iterable

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el