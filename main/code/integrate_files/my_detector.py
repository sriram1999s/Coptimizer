import sys
import re
import copy
import secrets
import uuid
import sys
sys.setrecursionlimit(10**9)
from parser_file import *
from function_inline import *

lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except :
    print('No arguments')

def get_defn_t_ix(fn_name):
    for ix in range(len(fn_defn_list)):
        if(fn_defn_list[ix][0] == fn_name):
            return ix

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
            #fn_call_list.pop(call_t_ix1 + 1)
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

def fn_inline_solve(i,n,z,cyc_chk,non_in_fn):
    #print("cyc_chk1 :",cyc_chk)
    if(i == n):
        return
    elif(type(z[i]) is tuple):
        if(z[i][2] == 'call'):
            call_t_ix = fn_call_list.index(z[i])
            defn_t_ix = get_defn_t_ix(z[i][0])
            if(fn_defn_obj_list[defn_t_ix].inline_flag == 1 and (z[i][0] not in cyc_chk)):
                name_fn = z[i][0]
                #---------------par_to_arg_match-----------------------------
                fn_body = copy.deepcopy(fn_defn_obj_list[defn_t_ix].body)
                #print(z[i][0],"fn_body :\n",fn_body,"\n\n")
                fn_body[0].pop(0)
                fn_body[0].pop(-1)

                #param_hash = secrets.token_hex(nbytes=12)
                param_hash = uuid.uuid4().hex
                parameter_list1 = copy.deepcopy(fn_defn_obj_list[defn_t_ix].param_list)
                parameter_list2 = get_param_vars(parameter_list1)
                add_param_hash(param_hash,parameter_list1)
                replace_param(0 , len(fn_body) , fn_body , parameter_list2 , param_hash)
                #print(z[i][0],"parameter_list1 : ",parameter_list1)
                par_arg_match = " "
                for ix in range(len(parameter_list1)):
                    param = parameter_list1[ix]
                    arg = fn_call_obj_list[call_t_ix].arg_list[ix]
                    #print(z[i][0],"param :",param,"type :",type(param),"arg :",arg,"type :",type(arg))
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
                #print("\nret_value :",z[i][0],ret_value,"\n")
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

                #print(z[i][0],"fn_bodyyy\n",fn_body)
                z.insert(i,fn_body)
                z.pop(i + 1)
                if(i + 1 < len(z) and fn_call_expr_flag == 4):
                    z.pop(i + 1)
                cyc_chk.append(name_fn)
                fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)
                if(cyc_chk != []):
                    cyc_chk.pop()
                '''if(cyc_chk != [] and cyc_chk[0] == name_fn):
                    cyc_chk = []'''
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
            #print("CAME HERE")
            defn_t_ix = get_defn_t_ix(z[i][0])
            fn_obj2 = fn_defn_obj_list[defn_t_ix];
            #print(fn_obj2.name)
            #print("defn :",z[i][0])
            fn_defn = z[i][1]
            z.insert(i,fn_defn)
            z.pop(i + 1)
            retrieve_defn(0,len(z[i]),z[i])

            '''if(fn_obj2.inline_flag == 0):
                print("defn :",z[i][0])
                fn_defn = z[i][1]
                z.insert(i,fn_defn)
                z.pop(i + 1)
                retrieve_defn(0,len(z[i]),z[i])'''
                #fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)

    elif(type(z[i]) is list):
        fn_inline_solve(0,len(z[i]),z[i],cyc_chk,non_in_fn)

    fn_inline_solve(i+1,len(z),z,cyc_chk,non_in_fn)

def transform_tuples(i,n,defn_list):
    if(i == n):
        return
    elif(type(defn_list[i]) is list):
        transform_tuples(0,len(defn_list[i]),defn_list[i])
    elif(type(defn_list[i]) is tuple):
        fn_call1 = []
        if(len(defn_list[i]) == 5):
            ret_dec = " " + defn_list[i][3] + " " + defn_list[i][4] + " = "
            fn_call1.append(ret_dec)
            fn_call1.append(defn_list[i][1])
            fn_call1.append(';')
        elif(len(defn_list[i]) == 4):
            ret_dec = " " + defn_list[i][3] + " = "
            fn_call1.append(ret_dec)
            fn_call1.append(defn_list[i][1])
            fn_call1.append(';')
        elif(len(defn_list[i]) == 6):
            if(defn_list[i][-1] == "return"):
                fn_call1 = defn_list[i][1]
                fn_call1.insert(0," return ")
            else :
                fn_call1 = defn_list[i][1]
                fn_call1.insert(0," " + defn_list[i][-1] + " ")
        else:
            fn_call1 = defn_list[i][1]
        defn_list.insert(i,fn_call1)
        defn_list.pop(i+1)

    transform_tuples(i + 1,len(defn_list),defn_list)

def remove_unwanted_defns(i,n,z,non_in_fn):
    if(i == n):
        return
    elif(type(z[i]) is list):
        remove_unwanted_defns(0,len(z[i]),z[i],non_in_fn)
    elif(type(z[i]) is tuple):
        if(z[i][0] not in non_in_fn):
            z.insert(i,"")
            z.pop(i + 1)
        else:
            defn_list = z[i][1]
            transform_tuples(0,len(defn_list),defn_list)
            z.insert(i,defn_list)
            z.pop(i + 1)
    remove_unwanted_defns(i + 1,len(z),z,non_in_fn)

#------------------------------------IO handling --------------------------------------------------------------------------

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z=parser.parse(lines)

#print("AST:")
#print(z)
print()
print()

fn_defn_list.sort(key = lambda x:x[0])
fn_defn_obj_list.sort(key = lambda x:x.name)
#fn_call_list.sort(key = lambda x:x[0])
#fn_call_obj_list.sort(key = lambda x:x.name)
cyc_chk = []
non_in_fn = []
print("\nz before : \n",z)
fn_inline_solve(0,len(z),z,cyc_chk,non_in_fn);
#remove_unwanted_defns(0,len(z),z,non_in_fn)
print("\nz after : \n",z)
output_prg=[]
solve(0,len(z),z,output_prg)
print("\n\nnon_in_fn : ",non_in_fn,"\n\n")
print("\n\nz :",z,"\n\n")
print("\n\noutput_prg : \n",output_prg,"\n\n")

with open("temp.c","w+") as f :
    f.write("".join(output_prg))
#print("generated code")
print("".join(output_prg))

#----------------------------------IO handling -----------------------------------------------------------------------------
