from function_inline import *
temp_list2 = []

def flatten1(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, (str, bytes)):
            yield from flatten1(el)
        else:
            yield el

def mark_tuples(i,n,z,num):
    if(i == n):
        return;
    elif(type(z[i]) is list):
        mark_tuples(0,len(z[i]),z[i],num)
    elif(type(z[i]) is tuple):
        fn_name = z[i][0]
        t1 = (fn_name,num[0])
        l = list(z[i])
        l[0] = t1
        l = tuple(l)
        z.insert(i,l)
        z.pop(i + 1)
        num[0] += 1

    mark_tuples(i + 1,len(z),z,num);

def verify_end(ix):
    bracket_count = 0;
    temp_list2_len = len(temp_list2);
    while(ix < temp_list2_len):
        if(temp_list2[ix] == "{"):
            bracket_count += 1;
        if(temp_list2[ix] == "}"):
            bracket_count -= 1;
            if(bracket_count == 0):
                return ix;
        ix += 1;

def lookback_for_loop(ix):
    loop_list = ["while", "for", "do"];
    end_pts = ["{", "}"];
    while(ix >= 0):
        if(temp_list2[ix] in end_pts):
            return 0;
        if(temp_list2[ix] in loop_list):
            return 1;
        ix -= 1;

def check_loop(ix):
    bracket_count = 1;
    while(ix >= 0):
        if(temp_list2[ix] == "}"):
            bracket_count += 1;
        if(temp_list2[ix] == "{"):
            bracket_count -= 1;
            if(bracket_count == 0):
                return lookback_for_loop(ix - 1);
        ix -= 1;

def check_tail_rec(ix):
    if(temp_list2[ix][-1] == "return"):
        return 1;
    ix += 1;
    temp_list2_len = len(temp_list2)
    while(ix < temp_list2_len):
        if(temp_list2[ix] == "else"):
            ix = verify_end(ix + 1)
        elif(temp_list2[ix] == ";"):
            ix += 1;
            continue;
        elif(temp_list2[ix] == "}"):
            res = check_loop(ix - 1);
            if(res == 1):
                return 0;
            ix += 1; continue;
        else:
            return 0;
        ix += 1;
    return 1;

def get_arg_list(parsed_list):
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
    return temp;

def converted(str, goto_hash, param_list1):
    len1 = len(param_list1);
    for ix in range(len1):
        str = re.sub('\\b' + param_list1[ix] + "\\b", "par_" + param_list1[ix] + "_" + goto_hash, str)
    return str;

def assignArgPar(arg_list, param_list, goto_hash):
    param_list1 = list(map(lambda str : str.split()[-1], param_list))
    str = ""
    len1 = len(arg_list)
    for ix in range(len1):
        type = param_list[ix].rpartition(' ')[0];
        str += type + " par_" + param_list1[ix] + "_" + goto_hash + " = " + param_list1[ix] + ";\n";

    for ix in range(len1):
        str += param_list1[ix] + " = " + converted(arg_list[ix], goto_hash, param_list1) + ";\n"
    return str;

def tail_rec_handler(i,n,z,fn_name):
    if(i == n):
        return;
    elif(type(z[i]) is list):
        tail_rec_handler(0,len(z[i]),z[i],fn_name)
    elif(type(z[i]) is tuple):
        if(z[i][0][0] == fn_name):
            temp_list2_ix = temp_list2.index(z[i]);
            res = check_tail_rec(temp_list2_ix)
            if(res == 1):
                # print("Tail rec call : ",z[i]);
                defn_t_ix = get_defn_t_ix(z[i][0][0]);

                arg_list = get_arg_list(z[i][1]);
                param_list = fn_defn_obj_list[defn_t_ix].param_list;

                rec_fn_body = fn_defn_obj_list[defn_t_ix].body[0];
                if(type(rec_fn_body[1]) is str and len(rec_fn_body[1]) >= 6 and rec_fn_body[1][0:6] == "label_"):
                    colon_ix = rec_fn_body[1].index(":")
                    goto_hash = rec_fn_body[6 : colon_ix];
                else:
                    goto_hash = uuid.uuid4().hex;
                    label_part = "label_" + goto_hash + ": {}\n"
                    rec_fn_body.insert(1,label_part);

                arg_par_assign_str = assignArgPar(arg_list, param_list, goto_hash);
                goto_block = "{ // tail recursion eliminated\n" + arg_par_assign_str;
                goto_block += "goto label_" + goto_hash + ";\n}"

                rec_fn_ret_type = fn_defn_obj_list[defn_t_ix].return_type;
                if(rec_fn_ret_type == "void" and "return" not in flatten(rec_fn_body)):
                    rec_fn_body.insert(-1,"return ;");

                z.insert(i,goto_block);
                z.pop(i + 1);

                # print("arg_list : ",arg_list);
                # print("param_list : ",param_list);
                # print("arg_par_assign_str : ",arg_par_assign_str);
                # print("goto_block : ",goto_block);
                # print("rec_fn_body : ", fn_defn_obj_list[defn_t_ix].body[0]);
                # # x_1212dfjhi2378 = 1

    tail_rec_handler(i + 1,len(z),z,fn_name);
