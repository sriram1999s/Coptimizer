from optimizations.tail_recc_elim import *
from multiprocessing import Pool
import copy
import secrets
import uuid
import sys
import re
import itertools
# temp_list1 = []
# temp_list2 = []

# ----------------------------------------------fn inliner -----------------------------------------------------------
'''function inlining recursive handler'''
def fn_inline_solve(i,n,z,cyc_chk,non_in_fn):
    ##print("cyc_chk1 :",cyc_chk)
    if(i == n):
        return
    elif(type(z[i]) is tuple):
        if(z[i][2] == 'call'):
            call_t_ix = fn_call_list.index(z[i])
            defn_t_ix = get_defn_t_ix(z[i][0])
            if(defn_t_ix != None and fn_defn_obj_list[defn_t_ix].inline_flag == 1 and (z[i][0] not in cyc_chk)):
                name_fn = z[i][0]
                #---------------par_to_arg_match-----------------------------
                fn_body = copy.deepcopy(fn_defn_obj_list[defn_t_ix].body)
                ##print(z[i][0],"fn_body :\n",fn_body,"\n\n")
                fn_body[0].pop(0)
                fn_body[0].pop(-1)

                #param_hash = secrets.token_hex(nbytes=12)
                param_hash = uuid.uuid4().hex
                parameter_list1 = copy.deepcopy(fn_defn_obj_list[defn_t_ix].param_list)
                parameter_list2 = get_param_vars(parameter_list1)
                add_param_hash(param_hash,parameter_list1)
                replace_param(0 , len(fn_body) , fn_body , parameter_list2 , param_hash)
                ##print(z[i][0],"parameter_list1 : ",parameter_list1)
                par_arg_match = " "
                for ix in range(len(parameter_list1)):
                    param = parameter_list1[ix]
                    arg = fn_call_obj_list[call_t_ix].arg_list[ix]
                    ##print(z[i][0],"param :",param,"type :",type(param),"arg :",arg,"type :",type(arg))
                    par_arg_match += (param + ' = ' + arg + ' ; ')

                par_arg_match += " "
                goto_flag = [0]
                if(fn_defn_obj_list[defn_t_ix].return_type != 'void'):
                    remove_return(0,len(fn_body),fn_body, param_hash)
                else:
                    label_hash = param_hash
                    remove_return1(0,len(fn_body),fn_body, label_hash,goto_flag)

                fn_body.insert(0,par_arg_match)
                fn_body.insert(0,' { // '+z[i][0]+' inlined \n')
                #---------------par_to_arg_match-----------------------------

                #---------------ret_val_to_ret_var_match---------------------
                return_type = fn_defn_obj_list[defn_t_ix].return_type;
                ret_val_str = ""
                some_temp = ""
                ret_value = fn_defn_obj_list[defn_t_ix].return_id_or_val
                ##print("\nret_value :",z[i][0],ret_value,"\n")
                fn_call_expr_flag = 0
                if(ret_value):
                    #if(ret_value in parameter_list2):
                    #    ret_value += "_" + param_hash
                    if(len(z[i]) == 5):
                        ret_dec = z[i][3] + " " + z[i][4] + " ;\n" + z[i][3] + " temp_" + param_hash + ";\n"
                        fn_body.insert(0,ret_dec)
                        fn_call_expr_flag = 5
                    elif(len(z[i]) == 4):
                        ret_dec = "\n" + return_type + " temp_" + param_hash + " ;\n"
                        fn_body.insert(0,ret_dec)
                        fn_call_expr_flag = 4
                    elif(len(z[i]) == 6):
                        ret_dec = "\n" + return_type + " temp_" + param_hash + " ;\n"
                        fn_body.insert(0,ret_dec)
                        if(z[i][-1] != "return"):
                            fn_call_expr_flag = 61
                        else:
                            fn_call_expr_flag = 62
                    else:
                        if(return_type != "void"):
                            ret_dec = "\n" + return_type + " temp_" + param_hash + " ;\n"
                            fn_body.insert(0,ret_dec)

                #---------------ret_val_to_ret_var_match--------------------

                fn_body.append(' }\n')
                if(goto_flag[0] == 1):
                    fn_body.append("label_" + label_hash + " : {}\n")
                if(fn_call_expr_flag == 5):
                    fn_body.append('\n' + z[i][4] + " = temp_" + param_hash + " ;\n")
                elif(fn_call_expr_flag == 4):
                    fn_body.append('\n' + z[i][3] + " = temp_" + param_hash + " ;\n")
                elif(fn_call_expr_flag == 61):
                    fn_body.append('\n' + z[i][-1] + " temp_" + param_hash + " ;\n")
                elif(fn_call_expr_flag == 62):
                    fn_body.append('\nreturn ' + "temp_" + param_hash + " ;\n")

                ##print(z[i][0],"fn_bodyyy\n",fn_body)
                z.insert(i,fn_body)
                z.pop(i + 1)
                if(i + 1 < len(z) and fn_call_expr_flag == 4):
                    z.pop(i + 1)
                cyc_chk.append(name_fn)
                fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)
                if(cyc_chk != []):
                    cyc_chk.pop()
            else:
                if(z[i][0] in cyc_chk):
                    fn_name = z[i][0]
                    ix2 = cyc_chk.index(fn_name)
                    non_in_fn += cyc_chk[ix2 : ]
                fn_call1 = []
                if(len(z[i]) == 5):
                    ret_dec = " " + z[i][3] + " " + z[i][4] + " = "
                    fn_call1.append(ret_dec)
                    fn_call1.append(z[i][1])
                    #fn_call1.append(';')
                elif(len(z[i]) == 4):
                    ret_dec = " " + z[i][3] + " = "
                    fn_call1.append(ret_dec)
                    fn_call1.append(z[i][1])
                    #fn_call1.append(';')
                elif(len(z[i]) == 6):
                    if(z[i][-1] == "return"):
                        fn_call1 = z[i][1]
                        fn_call1.insert(0," return ")
                    else :
                        fn_call1 = z[i][1]
                        fn_call1.insert(0," " + z[i][-1] + " ")
                else:
                    fn_call1 = z[i][1]
                z.insert(i,fn_call1)
                z.pop(i+1)
                fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)
        else:
            ##print("CAME HERE")
            defn_t_ix = get_defn_t_ix(z[i][0])
            fn_obj2 = fn_defn_obj_list[defn_t_ix];
            ##print(fn_obj2.name)
            ##print("defn :",z[i][0])
            fn_defn = z[i][1]
            z.insert(i,fn_defn)
            z.pop(i + 1)
            retrieve_defn(0,len(z[i]),z[i])

    elif(type(z[i]) is list):
        fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)

    fn_inline_solve(i+1,len(z),z,cyc_chk,non_in_fn)

# ----------------------------------------------tail-rec-elimination ------------------------------------------------------
'''tail recursion recursive handler'''
def tail_rec_eli_solve(in_flag1, i,n,z):
    global temp_list2
    if(i == n):
        return
    elif(type(z[i]) is tuple):
        if(z[i][2] == "definition"):
            defn_t_ix = get_defn_t_ix(z[i][0]);
            if(fn_defn_obj_list[defn_t_ix].inline_flag == 0):
                fn_name = fn_defn_obj_list[defn_t_ix].name;
                temp_list1 = fn_defn_list[defn_t_ix][1];

                mark_tuples(0,len(temp_list1),temp_list1,[1]);

                temp_list2 = list(flatten1(copy.deepcopy(temp_list1)))
                print("temp_list2 : ",temp_list2,"\n\n");
                tail_rec_controller(0,len(temp_list1),temp_list1,fn_name, temp_list2)

                revert_tuples(0,len(temp_list1), temp_list1)
                if(not in_flag1):
                    pl = z[i][1]
                    z.insert(i,pl);
                    z.pop(i + 1)
                    tail_rec_eli_solve(in_flag1, 0 ,len(z[i]), z[i])
            else:
                if(not in_flag1):
                    pl = z[i][1]
                    z.insert(i,pl);
                    z.pop(i + 1)
                    tail_rec_eli_solve(in_flag1, 0 ,len(z[i]), z[i])
        else:
            if(not in_flag1):
                pl = z[i][1]
                z.insert(i,pl)
                z.pop(i + 1)


    elif(type(z[i]) is list):
        tail_rec_eli_solve(in_flag1, 0,len(z[i]),z[i])

    tail_rec_eli_solve(in_flag1, i + 1,len(z),z)

# ----------------------------------------------tail-rec-elimination ------------------------------------------------------

# ----------------------------------------------code generator ------------------------------------------------------

# def solve(start_index, end_index, parse_tree, output_prg):
#     space_list = ['int','float','void','double','bool','char','return','else','if']
#     # space_list = ['return']
#     if(start_index == end_index):
#         return
#     elif(parse_tree[start_index]==None):
#          solve(start_index+1, end_index, parse_tree, output_prg)
#     elif(type(parse_tree[start_index]) is str):
#         if(start_index+1<end_index and parse_tree[start_index] in space_list and parse_tree[start_index+1]!=' '):
#             output_prg += [parse_tree[start_index], ' ']
#         else:
#             output_prg += [parse_tree[start_index]]
#         solve(start_index+1, end_index, parse_tree, output_prg)
#     elif(type(parse_tree[start_index]) is int):
#         output_prg += [str(parse_tree[start_index])]
#         solve(start_index+1, end_index, parse_tree, output_prg)
#
#     elif(type(parse_tree[start_index]) is tuple or type(parse_tree[start_index]) is list):
#         for trav in range(len(parse_tree[start_index])):
#             if(parse_tree[start_index][trav]==None):
#                 continue
#             elif(type(parse_tree[start_index][trav]) is tuple or type(parse_tree[start_index][trav]) is list):
#                 solve(0, len(parse_tree[start_index][trav]), parse_tree[start_index][trav], output_prg)
#             else:
#                 print("in solve ", parse_tree[start_index], trav + 1, end_index)
#                 if(trav+1<end_index and parse_tree[start_index][trav] in space_list and parse_tree[start_index][trav+1]!=' '):
#                     output_prg += [parse_tree[start_index][trav], ' ']
#                 else:
#                     output_prg += [str(parse_tree[start_index][trav])]
#         solve(start_index+1, end_index, parse_tree, output_prg)

'''recursive regenerator'''
def solve(start_index, end_index, parse_tree):
    space_list = ['int','float','void','double','bool','char','return','else','if','struct']
    '''base case when index has reached the end'''
    if(start_index == end_index):
        return []
    '''continue recursion'''
    elif(parse_tree[start_index]==None):
             return solve(start_index+1, end_index, parse_tree)
    '''solve for string and continue recursion'''
    elif(type(parse_tree[start_index]) is str):
            '''space inserted in case the string belongs to space_list'''
            if(start_index+1<end_index and parse_tree[start_index] in space_list and parse_tree[start_index+1]!=' '):
                output_prg = [parse_tree[start_index], ' ']
            else:
                output_prg = [parse_tree[start_index]]
            return output_prg + solve(start_index+1, end_index, parse_tree)
    '''handle appending if element is int and continue recursion'''
    elif(type(parse_tree[start_index]) is int):
        output_prg = [str(parse_tree[start_index])]
        return output_prg + solve(start_index+1, end_index, parse_tree)
    '''recurse into the sublist if type is list'''
    elif(type(parse_tree[start_index])==list):
        return solve(0, len(parse_tree[start_index]), parse_tree[start_index]) + solve(start_index+1, end_index, parse_tree)
    


'''multi threaded solve (Buggy)'''
def solve_multithread(start_index,end_index,parse_tree):
    workers = 3
    p = Pool(workers)
    slices = [parse_tree[i::workers] for i in range(workers)]
    len_slices = [len(i) for i in slices]
    output_worker = p.starmap(solve,list(zip(itertools.repeat(0),len_slices,slices)))
    p.close()
    p.join()
    output_prg = []
    for output in output_worker:
        output_prg += output

    return output_prg

    # return result
# -----------------------------------------------------------------------------------------------------------------------
