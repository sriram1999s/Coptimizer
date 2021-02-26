def dummy_fn():
    print("YO")


fn_defn_list = []  # list of tuple of fn_defn having parsed list and "defn"
fn_defn_obj_list = []  # list of objects having function definition details

fn_call_list = []  # list of tuple of fn_call having parsed list and "call"
fn_call_obj_list = []  # list of objects having function call details


def inline_defn_helper(parsed_list):
    fn_defn_list.append((parsed_list, "definition"))
    create_defn_obj(parsed_list)


def create_defn_obj(parsed_list):
    obj = fn_defn_class(parsed_list[1], parsed_list[3], parsed_list[5])
    fn_defn_obj_list.append(obj)


def call_helper(parsed_list):
    fn_call_list.append((parsed_list, "call"))
    create_call_obj(parsed_list)


def create_call_obj(parsed_list):
    obj1 = fn_call_class(parsed_list[0], parsed_list[2])
    fn_call_obj_list.append(obj1)


class fn_defn_class:
    def __init__(self, name, param_list, body):
        self.name = name
        self.param_list = param_list
        self.body = body
        self.inline_flag = 0
        self.return_id_or_val = None


class fn_call_class:
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list
