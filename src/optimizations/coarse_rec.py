from optimizations.function_inline import *
import secrets

'''
fn_defn_list # list of tuple of fn_defn having parsed list and "defn"
fn_defn_obj_list # list of objects having function definition details

fn_call_list # list of tuple of fn_call having parsed list and "call"
fn_call_obj_list # list of objects having function call details
'''

num_rule_applied = 0
redundant_params = "FRAME_COUNT, FRAME_LIMIT, head_, ptr_block"

def flatten_except_t(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, (str, bytes)):
            yield from flatten_except_t(el)
        else:
            yield el

def check_CR(fn_defn_t):
    given_fn_name = fn_defn_t[0]
    # fn_defn_t[1] : the given fn in parsed list format
    temp_flat = flatten_except_t(fn_defn_t[1])

    ''' return 1 if there's >= 1 recursive call and no call to other fns '''
    ''' Must be refined later '''
    num_rec_calls = 0
    for ele in temp_flat:
        if isinstance(ele, tuple):
            # dealing with a fn_call tuple
            if ele[0] == "printf" or ele[0] == "scanf":
                continue
            if ele[0] != given_fn_name:
                return 0
            num_rec_calls += 1

    if num_rec_calls > 0:
        return 1
    return 0

def ast_to_str(ast):
    ast = list(flatten_except_t(ast))
    ast = [str(ele) if not isinstance(ele, (tuple, list)) else ele for ele in ast]

    for ix, ele in enumerate(ast):
        if type(ele) is tuple:
            ast[ix] = [str(ele1) if not(type(ele1) is str) else ele1 for ele1 in flatten_except_t(ele[1])]
            ast[ix] = " ".join(ast[ix])

    return " ".join(ast)

match_list = []

def placeholder_callable(m):
    global match_list
    temp = m.group(1) + "placeholder"
    match_list.append(m.group(2))
    return temp

def trampolineFN_callable(m):
    global redundant_params
    global match_list
    temp = m.group(2)[:-1].strip()
    if temp[-1] != '(':
        temp += ', '

    match_list.append(temp)

    return m.group(1) + temp + redundant_params + ')'

def replace_curr_fn(i, n, z, fn_defn_t, four_const_list):
    if i == n:
        return

    if type(z[i]) is list:
        replace_curr_fn(0, len(z[i]), z[i], fn_defn_t, four_const_list)

    if type(z[i]) is tuple:
        if z[i][2] == "call":
            fn_call1 = []
            if(len(z[i]) == 5):
                ret_dec = " " + z[i][3] + " " + z[i][4] + " = "
                fn_call1.append(ret_dec)
                fn_call1.append(z[i][1])
            elif(len(z[i]) == 4):
                ret_dec = " " + z[i][3] + " = "
                fn_call1.append(ret_dec)
                fn_call1.append(z[i][1])
            elif(len(z[i]) == 6):
                if(z[i][-1] == "return"):
                    fn_call1 = z[i][1]
                    fn_call1.insert(0," return ")
                else :
                    fn_call1 = z[i][1]
                    fn_call1.insert(0," " + z[i][-1] + " ")
            else:
                fn_call1 = z[i][1]

            z.insert(i, fn_call1)
            z.pop(i + 1)
        else:
            if z[i] == fn_defn_t:
                z.insert(i, four_const_list)
                z.pop(i + 1)
            else:
                temp = z[i][1]
                z.insert(i, temp)
                z.pop(i + 1)

    replace_curr_fn(i + 1, n, z, fn_defn_t, four_const_list)

def add_constructs(fn_defn_t, z):
    fn_name = fn_defn_t[0]
    hash = secrets.token_hex(nbytes = 4)
    MAX_SIZE = 100000000
    # MAX_SIZE = "INT_MAX"

    ''' getting the param_declarations for the given fn_defn '''
    # the defn_obj for the given fn_defn_t
    fn_defn_obj = next(defn_obj for defn_obj in fn_defn_obj_list if defn_obj.name == fn_defn_t[0])

    ret_type = fn_defn_obj.return_type
    struct_type = f"node_{fn_name}_{hash}_t"

    actual_param_list = fn_defn_obj.param_list
    par_list_c = ", ".join(actual_param_list)
    param_decls = ";\n".join(actual_param_list) + ";\n"
    # + f"{struct_type} next;"

    ''' generate a struct defn to maintain a dynamic array on the heap '''
    struct_str = f'''
    typedef struct node_{fn_name}_{hash}
    {{
        {param_decls}
    }} {struct_type};
    '''

    ''' generate a wrapper fn '''
    temp = (par.split()[-1] for par in actual_param_list)
    par_name_list = [par_name.replace('*', '') for par_name in temp]
    new_par_list = f"{'' if not actual_param_list else (', '.join(par_name_list) + ', ')}" + "FRAME_COUNT, FRAME_LIMIT, head_, ptr_block"
    ptrTOblockOf0_par_names = [f"ptr_block[0].{par}" for par in par_name_list]
    same_par_list = f"{'' if not actual_param_list else (', '.join(ptrTOblockOf0_par_names) + ', ')}" + "FRAME_COUNT, FRAME_LIMIT, head_, ptr_block"

    node_par = ""
    node_par = ", ".join(f"ptr_block[ix].{ele}" for ele in par_name_list)
    if ret_type != 'void':
        # placeholder var exists only when there's a return result
        node_par += ', '

    par_name_list2 = new_par_list.split(', ')[:-4]
    save_state_inits = "\t".join(f"ptr_block[0].{par} = {par};\n" for par in par_name_list2)

    wrapper_str = f'''
    {ret_type} {fn_name}({par_list_c})
    {{
        // all necessary initializations
        {struct_type}* ptr_block = ({struct_type}*) malloc(sizeof({struct_type}) * {MAX_SIZE});
        int* head_ = (int*) malloc(sizeof(int));
        *head_ = 0;
        int FRAME_COUNT = 0;
        int FRAME_LIMIT = 1000;

        {save_state_inits}

        int status = setjmp(buf);

        // status = 0 : 1st time execution
        // status = 1 : execution after return from trampoline top

        {ret_type + " result_ = " if ret_type != "void" else ""}{fn_name}_{hash}({same_par_list});

        // computation
        {ret_type  + ' pvar_' + hash + ';' if ret_type != "void" else ""}
        {ret_type  + ' finalRes_' + hash + ';' if ret_type != "void" else ""}
        int ix = *head_;
        while(ix)
        {{
            {'finalRes_' + hash + ' =' if ret_type != 'void' else ''} placeholder_{hash}({node_par}{'pvar_' + hash if ret_type != 'void' else ''} );
            {'pvar_' + hash + ' = finalRes_' + hash + ';' if ret_type != 'void' else ''}
            ix -= 1;
        }}

        free(head_);
        free(ptr_block);
        {"return finalRes_" + hash + ';' if ret_type != "void" else ""}
    }}
    '''

    ''' generate a tarmpoline fn '''
    fn_defn_ast = copy.deepcopy(fn_defn_t[1])
    defn_str = ast_to_str(fn_defn_ast)

    import re
    global match_list; global redundant_params
    defn_str_placeholder = re.sub(fr"(.*?)({fn_name}\s*\(.*?\))", placeholder_callable, defn_str)
    fn_proto = match_list[0]

    match_list = []
    defn_str_trampolineFN = re.sub(fr"(.*?)({fn_name}\s*\(.*?\))", trampolineFN_callable, defn_str)

    defn_str_trampolineFN = defn_str_trampolineFN.replace(match_list[0] + redundant_params + ')', match_list[0] + f"int FRAME_COUNT, int FRAME_LIMIT, int* head_, {struct_type}* ptr_block" + ")", 1)
    # defn_str_trampolineFN = defn_str_trampolineFN.replace(fr"\b{fn_name}\b", f"{fn_name}_{hash}")

    defn_str_trampolineFN = re.sub(fr"\b{fn_name}\b", f"{fn_name}_{hash}", defn_str_trampolineFN)

    defn_str_trampolineFN = defn_str_trampolineFN.strip()

    node_inits = "\t".join(f"ptr_block[*head_].{par} = {par};\n" for par in par_name_list2)

    trampoline_c12 = f'''
    if(FRAME_COUNT == FRAME_LIMIT)
    {{
        // save state in the first node, for the next subsequent node
        {save_state_inits}
        longjmp(buf, 1);
    }}

    FRAME_COUNT += 1; *head_ += 1;
    {node_inits}
    '''

    try:
        trampoline_c3 = re.search(r"{.*}", defn_str_trampolineFN).group(0)
    except Exception as e:
        print("match : None", e)

    defn_str_trampolineFN = f'''
    {ret_type} {fn_name}_{hash}({", ".join(actual_param_list) + ", " if actual_param_list else ""}int FRAME_COUNT, int FRAME_LIMIT, int* head_, {struct_type}* ptr_block)
    {{
        {trampoline_c12}
        {trampoline_c3}
    }}
    '''

    ''' generate a placeholder fn '''
    # fn_proto = f"placeholder_{hash} ({', '.join(actual_param_list) + ', ' if actual_param_list else ''}" + f"{ret_type} placeholder)"

    fn_proto = ""
    if ret_type != "void":
        fn_proto = f"placeholder_{hash} ({', '.join(actual_param_list) + ', ' if actual_param_list else ''}" + f"{ret_type} placeholder)"
    else:
        # for void ret_types
        fn_proto = f"placeholder_{hash} ({', '.join(actual_param_list) if actual_param_list else ''}" + ")"

    defn_str_placeholder = defn_str_placeholder.replace('placeholder', fn_proto, 1)
    if ret_type == "void":
        defn_str_placeholder = re.sub(r"placeholder\s*[;\s]+?", "", defn_str_placeholder)

    global num_rule_applied
    if num_rule_applied == 0:
        req_headers = f'''#include<stdio.h>
        #include<stdlib.h>
        #include<setjmp.h>
        #include<limits.h>

        jmp_buf buf;
        '''
        z.insert(0, req_headers)

    four_const_list = [struct_str, defn_str_placeholder, defn_str_trampolineFN, wrapper_str]
    replace_curr_fn(0, len(z), z, fn_defn_t, four_const_list)

    print("\n\n z : \n", z, '\n')

def coarse_rec_handler(z):
    global num_rule_applied
    # z : AST of the input code

    ''' check for each fn_defn if this rule is possible '''
    for fn_defn_t in fn_defn_list:
        cr_flag = check_CR(fn_defn_t)

        if not cr_flag:
            # can't apply rule
            ''' get this fn_defn out of it's tuple '''
            print("\n Didn't perform on : ", fn_defn_t[0])
            continue

        print("\n Did perform on : ", fn_defn_t[0])
        # can apply rule by adding some constructs
        add_constructs(fn_defn_t, z)
        num_rule_applied += 1
