def dummy_fn():
    print("YO")


fn_defn_list = []  # list of tuple of fn_defn having parsed list and "defn"
fn_defn_obj_list = []  # list of objects having function definition details

fn_call_list = []  # list of tuple of fn_call having parsed list and "call"
fn_call_obj_list = []  # list of objects having function call details


def inline_defn_helper(parsed_list):
    fn_defn_list.append((parsed_list, "definition"))
    create_defn_obj(parsed_list)
    if fn_defn_obj_list[-1].inline_flag == 0:    # not inlinable
        return (parsed_list, 'definition')
    else:   #inlinable
        return None

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
# ["int a","int b"]

def create_defn_obj(parsed_list):

    l3 = [1]
    check_inline(parsed_list[5][0], 0, len(parsed_list[5][0]), parsed_list[1], l3)
    inline_flag = l3[0]
    print('#inline flag', inline_flag, parsed_list[1])
    
    # needs change
    return_id_or_val = check_return(parsed_list[5][0], 0, len(parsed_list[5][0]))

    str_params_list = change_to_string(parsed_list[3])

    obj = fn_defn_class(parsed_list[1], str_params_list, parsed_list[5], inline_flag, return_id_or_val)
    fn_defn_obj_list.append(obj)
    print("Fn defn obj",obj.name,obj.param_list,obj.body,obj.inline_flag,obj.return_id_or_val,sep="\n")


def call_helper(parsed_list):
    fn_call_list.append((parsed_list, "call"))
    create_call_obj(parsed_list)


def create_call_obj(parsed_list):
    temp = []
    for i in parsed_list[2]:
        if i != ',':
            temp.append(str(i))
    obj1 = fn_call_class(parsed_list[0], temp)
    fn_call_obj_list.append(obj1)
    #print("Fn call obj : \n",obj1.name,"\n",obj1.arg_list,"\n")


class fn_defn_class:
    def __init__(self, name, param_list, body, inline_flag, return_id_or_val):
        self.name = name
        self.param_list = param_list
        self.body = body
        self.inline_flag = inline_flag  # 0 => don't inline, 1 => inline
        self.return_id_or_val = return_id_or_val


class fn_call_class:
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list
