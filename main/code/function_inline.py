def dummy_fn():
    print("YO")


fn_defn_list = []  # list of tuple of fn_defn having parsed list and "defn"
fn_defn_obj_list = []  # list of objects having function definition details

fn_call_list = []  # list of tuple of fn_call having parsed list and "call"
fn_call_obj_list = []  # list of objects having function call details


def inline_defn_helper(parsed_list):
    fn_defn_list.append((parsed_list, "definition"))
    create_defn_obj(parsed_list)


def check_recursive(l1, start, length, fn_name):
    if start >= length:
        return 1
    if type(l1[start]) == str and l1[start] == fn_name:
        return 0
    elif type(l1[start]) == list:
        for i in l1[start]:
            if type(i) == list and check_recursive(i, 0, len(i), fn_name) == 0:
                return 0
    start += 1
    return check_recursive(l1, start, length, fn_name)


def create_defn_obj(parsed_list):
    # print('Body', parsed_list[5][0])
    inline_flag = check_recursive(parsed_list[5][0], 0, len(parsed_list[5][0]), parsed_list[1])
    print('rec flag', inline_flag)
    obj = fn_defn_class(parsed_list[1], parsed_list[3], parsed_list[5], inline_flag)
    fn_defn_obj_list.append(obj)


def call_helper(parsed_list):
    fn_call_list.append((parsed_list, "call"))
    create_call_obj(parsed_list)


def create_call_obj(parsed_list):
    obj1 = fn_call_class(parsed_list[0], parsed_list[2])
    fn_call_obj_list.append(obj1)


class fn_defn_class:
    def __init__(self, name, param_list, body, inline_flag):
        self.name = name
        self.param_list = param_list
        self.body = body
        self.inline_flag = inline_flag  # 0 => don't inline, 1 => inline
        self.return_id_or_val = None


class fn_call_class:
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list
