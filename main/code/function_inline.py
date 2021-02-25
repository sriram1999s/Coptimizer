def dummy_fn():
    print("YO")


fn_defn_list = []  # list of set of fn_defn as parsed list and "defn"
fn_defn_obj_list = []  # list of objects having function definition details

fn_call_list = []  # list of set of fn_call as parsed list and "call"
fn_call_obj_list = []  # list of objects having function call details


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
