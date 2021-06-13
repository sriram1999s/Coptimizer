from regenerator import *
from math import *
from optimizations.symboltable import *
from optimizations.loop_jamming import *
from collections import *
import re
import secrets
import random

list_looping_variables = defaultdict(lambda:0)
loop_var_flags = {}

# TODO

# 1) integerate check fxn with add
# 2) test it pls


'''checks whether unrolling is possible and calls appropriate fxn'''
def for_unroll_validate(OPTIMIZE1, OPTIMIZE2, sub_tree, nested):
    if(not OPTIMIZE1 and not OPTIMIZE2):
        return sub_tree
    #print("\n sub tree in unroll :\n", sub_tree)
    condition = sub_tree[1]
    # print("condition[2:]: ", condition[2:])
    # print("sub_tree[2]",sub_tree[2])
    operators = []
    find_operator(0, len(condition[-2]), condition[-2], operators)
    ids = dict()
    if nested:
        find_id(0, len(condition), condition, ids)
    else:
        find_id(0, len(condition[2:]), condition[2:], ids)

    loop_var = list(ids.keys())[0]
    if(loop_var not in loop_var_flags or not loop_var_flags[loop_var]):
        print("\n\nloop_var_flag problem\n\n")
        return sub_tree

    list_looping_variables[loop_var+'_'.join(sym_tab.level_str)]=1

    loop_var_dict = dict()
    find_id(0,len(sub_tree[2]),sub_tree[2],loop_var_dict)
    loop_var_list = list(loop_var_dict.keys())+[loop_var]

    #checking for pointers in loop body and adding what they refer to before taking intersection
    pointers = []
    for i in loop_var_list:
        search_string = sym_tab.make_level_string('*' + i)
        if(sym_tab.symbol_table[search_string]!='garbage'):
            pointers.append(sym_tab.symbol_table[search_string])

    loop_var_list+=pointers
    #print("loop_var_list: ",loop_var_list)
    # print("ids.keys(): ",list(ids.keys()))
    intersection = list(set(list(ids.keys()))&set(loop_var_list))
    #print("intersection: ",intersection)

    if(len(intersection)>1):
        return sub_tree

    # This part is changed so that loop variable will not be caught here (TODO major bug)
    if(len(intersection)==1):
        print("\n\nintersection problem loop_var\n\n",loop_var_list)
        for tok in loop_var_list:
            if(tok!=loop_var and loop_var_list.count(tok)>1):
                return sub_tree

    res = []
    find_int(0, len(condition), condition, res)
    # print("operators : ", operators)
    solve_substi_id(0,len(condition),condition,intersection)
    solve_expr(0,len(condition),condition)

    # print("condition: ", condition,"\n")

    ids=dict()
    find_id(0, len(condition), condition, ids)
    #print("ids : ",ids)
    if(len(ids) > 1):# more than 1 loop variable in condition, short circuit return
        # return sub_tree
        return for_variable_unroll(OPTIMIZE1,OPTIMIZE2,sub_tree,operators,ids,loop_var)

    if(not OPTIMIZE1):
        return sub_tree

    operator_list = ['++', '--', '/', '*', '+', '-', '+=', '-=', '*=', '/=']
    # checking for operators
    if(len(operators) > 0 and operators[0][0] not in operator_list):
        return sub_tree

    if(condition[1] != ';' and condition[2] != ';' and len(condition) == 5):  # full for condition
        return for_full_condition(sub_tree, operators, ids)
    elif(condition[2] == ';'):  # bounds check missing
        return sub_tree
    else:
        reconstruct_for(sub_tree, loop_var)
        if(sub_tree[1][3] == ')'):
            return sub_tree
        return for_full_condition(sub_tree, operators, ids)

# def substi_id(var):
#
#
#     search_str = var + '_'.join(sym_tab.level_str)
#     if(type(sym_tab.symbol_table[search_str]) == int):
#         return sym_tab.symbol_table[search_str]
#     return 'garbage'

'''check whether type of variable is list (helper fxn)'''
def check_type(l):
    for i in l:
        if(type(i) == list):
            return 0
    return 1

''' substi values for variables from symbl table '''
def solve_substi_id(i,n,l,loop_var):
    if(i==n):
        return
    if(type(l)==list and (len(l)==3 or len(l)==5) and check_type(l)):
        walk = [0,2]
        if(len(l)==5):
            walk = [1,3]
        for j in walk:
            if(type(l[j])==str and l[j] not in loop_var):
                search_str = l[j] + '_'.join(sym_tab.level_str)
                if(type(sym_tab.symbol_table[search_str]) == int):
                    l[j] = sym_tab.symbol_table[search_str]

    if(type(l[i])==list and (len(l[i])==3 or len(l[i])==5) and check_type(l[i])):
        walk = [0,2]
        if(len(l[i])==5):
            walk = [1,3]
        for j in walk:
            if(type(l[i][j])==str and l[i][j] not in loop_var):
                search_str = l[i][j] + '_'.join(sym_tab.level_str)
                if(type(sym_tab.symbol_table[search_str]) == int):
                    l[i][j] = sym_tab.symbol_table[search_str]
    if(type(l[i])==list):
        for j in l:
            if(type(j)==list):
                solve_substi_id(0,len(j),j,loop_var)
    solve_substi_id(i+1,n,l,loop_var)

''' solves arithmetic expressions if values available at compile time '''
def solve_expr(i,n,l):
    if(i==n):
        return
    if(type(l[i])==list and len(l[i])==3 and type(l[i][0])==int and type(l[i][1])==str and type(l[i][2])==int):
        if(l[i][1]=='+'):
            l[i] = l[i][0] + l[i][2]
        elif(l[i][1]=='-'):
            l[i] = l[i][0] - l[i][2]
        elif(l[i][1]=='*'):
            l[i] = l[i][0] * l[i][2]
        elif(l[i][1]=='/'):
            l[i] = l[i][0] / l[i][2]
        elif(l[i][1]=='&'):
            l[i] = l[i][0] & l[i][2]
        elif(l[i][1]=='|'):
            l[i] = l[i][0] | l[i][2]
        elif(l[i][1]=='^'):
            l[i] = l[i][0] ^ l[i][2]
        elif(l[i][1]=='<<'):
            l[i] = l[i][0] << l[i][2]
        elif(l[i][1]=='>>'):
            l[i] = l[i][0] >> l[i][2]

    if(type(l[i])==list):
        for j in l:
            if(type(j)==list):
                solve_expr(0,len(j),j)
    solve_expr(i+1,n,l)


''' checking for full_unrolling() '''
def for_full_condition(sub_tree, operators, ids):
    condition = sub_tree[1]
    output = []
    type_list = ['int ', 'float ', 'void ', 'double ', 'char ']

    # LHS or RHS of bounds check is not an expression
    if(type(condition[2][0][0]) == list or type(condition[2][0][2]) == list):
        # print("Here3-----")
        return sub_tree

    if(type(condition[2][0][2]) == str):
        temp = substi_id(condition[2][0][2])
        if(temp != 'garbage'):
            condition[2][0][2] = temp
        else:
            return sub_tree
            # return sub_tree

    res = []
    find_int(0, len(condition), condition, res)
    total = abs(res[1][0]-res[0][0])
    #print(res)
    if(type(condition[2][0][2]) == int):  # LHS of bounds check is an integer
        if(total <= 35):  # full unrolling
            # remove nesting in sub_tree[2]
            output = solve(0, len(sub_tree[2]), sub_tree[2])
            unrolled = for_full_unroll(output, condition, operators[0][0],res)
            res = [unrolled]
        else:
            output = solve(0, len(sub_tree[2]), sub_tree[2])
            unrolled = for_partial_unroll(output, condition, operators[0][0],res)
            res = [sub_tree[0], sub_tree[1], unrolled]
    return res

''' full unrolling '''
def for_full_unroll(block, condition, operator, res):
    print("Unrolling full...\n")
    block.pop(0)
    block.pop()
    # print('operator : ', operator)
    #res = []
    # to get start and end value of loop by scanning for integer
    #find_int(0, len(condition), condition, res)
    increment_val = 1
    if(len(res) == 3):
        increment_val = res[-1][0]
    if(re.search('[+-]', operator)):
        count_unrolls = int(ceil(abs(res[0][0]-res[1][0])/increment_val))
    else:
        count_unrolls = int(my_log(res[0][0], res[1][0], increment_val))
    if(block != [';']):
        block = ['{'] + block + ['}']
    return  block * count_unrolls


''' partial unrolling'''
def for_partial_unroll(block, condition, operator,res):
    print("Unrolling partial...\n")
    block.pop(0)
    block.pop()
    # print(f"operator : {operator}")
    #res = []
    increment_val = 1
    #find_int(0, len(condition), condition, res)
    # print(res)
    total = abs(res[0][0]-res[1][0])
    if(len(res) == 3):
        increment_val = res[-1][0]
    if(re.search('[+-]', operator)):
        count_unrolls = int(ceil(total/increment_val))
    else:
        count_unrolls = int(my_log(res[0][0], res[1][0], increment_val))
    factor = 0.2
    rel_operator = []
    find_rel_operator(0, len(condition[2]), condition[2], rel_operator)
    unroll_count = int(count_unrolls*factor)
    if(rel_operator[0][0] == '<'):  # readjusting the end value of loop after partial unrolling
        if(re.search('[+-]', operator)):
            condition[2][0][res[1][-1]] = res[0][0] + \
                (count_unrolls//unroll_count)*increment_val
        else:
            condition[2][0][res[1][-1]] = res[0][0] + \
                (count_unrolls//unroll_count)**increment_val

    else:
        if(re.search('[+-]', operator)):
            condition[2][0][res[1][-1]] = res[0][0] - \
                (count_unrolls//unroll_count)*increment_val
        else:
            condition[2][0][res[1][-1]] = res[0][0] - \
                (count_unrolls//unroll_count)**increment_val
    extra = count_unrolls % unroll_count

    if(block != [';']):
        block = ['{'] + block + ['}']

    return ['{']+block*unroll_count+['}'] + block*extra


# to be changed
# loop : 0 -> (n-(n%2))
# if(n%2):
#     unroll remaining
'''for_variable_unroll() ------> when the limits are decided at runtime'''
def for_variable_unroll(OPTIMIZE1,OPTIMIZE2,sub_tree,operator,ids,loop_var):
    #print("\n\nhey\n\n")
    if(operator[0][0] in ['/=','*=','*','/']):
        return sub_tree

    condition = sub_tree[1]
    lower_limit_str = []
    upper_limit_str = []
    increment_str = []
    lower_limit_str = solve(0,len(condition[1]),condition[1])
    upper_limit_str = solve(0,len(condition[2]),condition[2])
    increment_str = solve(0,len(condition[3]),condition[3])
    m = re.search('=(.*?);',''.join(lower_limit_str))
    lower_limit = m.group(1)
    if(re.search('^[0-9]*$',lower_limit)):
        lower_limit = int(lower_limit)
    m1 = re.search('([<>])(.*?);',''.join(upper_limit_str))
    upper_limit = m1.group(2)
    if(re.search('^[0-9]*$',upper_limit)):
        upper_limit = int(upper_limit)

    if(type(lower_limit)==str):
        if(list_looping_variables[sym_tab.make_level_string(lower_limit)]):
            return sub_tree

    if(type(upper_limit)==str):
        if(list_looping_variables[sym_tab.make_level_string(upper_limit)]):
            return sub_tree


    increment_val = '1'
    #print(''.join(increment_str))
    m2 = re.search('=(.*)',''.join(increment_str))
    if(m2):
        # print(m2.groups())
        increment_val=m2.group(1)

    #print("increment val:",increment_val)
    if(m1.group(1)=='>'):
        lower_limit,upper_limit = upper_limit,lower_limit

    if(OPTIMIZE2):
        #print("\nOPtimize 2 baaro magan!\n")
        jam.add(lower_limit, upper_limit, increment_val, sym_tab.level_str.copy(), sub_tree)
        with open("check.c","w") as f:
            f.write(gen_check(jam._worst_case))
    if(not OPTIMIZE1):
        return sub_tree



    # print("lower_limit: ",lower_limit,type(lower_limit))
    # print("upper_limit: ",upper_limit,type(upper_limit))

    lower_limit = '(' + str(lower_limit) + ')'

    modified_upper_limit_1 = '('+'(' + str(upper_limit) + '-' + str(lower_limit) + ')' + '/' + str(increment_val) + ')'
    modified_upper_limit_2 = '(' + '('+'(' + str(upper_limit) + '-' + str(lower_limit) + ')' + '%' + str(increment_val) + ')' + '!=0' +')'
    modified_upper_limit = '(' + modified_upper_limit_1 + '+' + modified_upper_limit_2 + ')'
    # print("modified_upper_limit: ",modified_upper_limit)


    tempesh_randesh_hashesh = 'temp_'+secrets.token_hex(nbytes=16)
    #tempesh_randesh_hashesh = 'temp_'+ str(random.randint(1,100))
    temp_loop_var = 'temp_loop_'+secrets.token_hex(nbytes=16)
    #temp_loop_var = 'temp_loop_'+ str(random.randint(1,100))
    sub_from_upper = '(' + tempesh_randesh_hashesh + '%' + '2' + ')'

    effective_upper_limit  = '(' + tempesh_randesh_hashesh + '-' + sub_from_upper + ')'+ '/' +'2'
    # print("effective_upper_limit",effective_upper_limit)

    body = []
    body = solve(0,len(sub_tree[2]),sub_tree[2])

    body  = ''.join(body)
    # print("body: ",body)

    declarations = f'int {tempesh_randesh_hashesh} = {modified_upper_limit};int {temp_loop_var};'
    temp_declaration  ='{' + f'{temp_loop_var} = {loop_var};' + '}'
    new_for_loop = f'for(int {loop_var} = 0 ; {loop_var} < {effective_upper_limit} ;  {loop_var}++)' + '{'+temp_declaration + body*2 + '}'
    def rep_sub(m):
        return m.group(1) + temp_loop_var + m.group(2)

    pat = '(\W)'+str(loop_var)+r'(\W)'
    body = re.sub(pat,rep_sub,body)
    remaining = f'if({sub_from_upper})' + '{' + body + '}'
    return declarations + new_for_loop + remaining


'''replace_string() ------> given a pat and target substi for target whenever pat is matched in nested iterables'''
def replace_string(i,n,l,pat,target):
    if(i==n):
        return
    if(l[i]==pat):
        l[i]=target
    if(type(l[i])==list):
        replace_string(0,len(l[i]),l[i],pat,target)
    replace_string(i+1,n,l,pat,target)


'''find_int()-----> scans for Integers in loop condition'''
def find_int(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) is int):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_int(0, len(lis[ind]), lis[ind], res)
    find_int(ind+1, end, lis, res)



'''find_operator()-----> scans for binary operators in loop condition'''
def find_operator(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) == str and re.search('[-+*/]', lis[ind])):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_operator(0, len(lis[ind]), lis[ind], res)
    find_operator(ind+1, end, lis, res)

'''find_rel_operator()-----> scans for rel operator in loop condition'''
def find_rel_operator(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) == str and re.search('[<>]', lis[ind])):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_rel_operator(0, len(lis[ind]), lis[ind], res)
    find_rel_operator(ind+1, end, lis, res)

'''find_id()-----> scans for variables in loop condition'''
def find_id(ind, end, lis, res=dict()):
    if(ind == end):
        return
    type_list = ['int', 'float', 'void', 'double', 'char']
    if(type(lis[ind]) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', lis[ind]) and lis[ind] not in type_list):
        res[lis[ind]]=0
    elif(type(lis[ind]) is list):
        find_id(0, len(lis[ind]), lis[ind], res)
    find_id(ind+1, end, lis, res)

''' reconstruct for condition from partial condition '''
def reconstruct_for(sub_tree, loop_var):
    # sub_tree[1][1]
    # print(sub_tree[1][1])

    search_str = sym_tab.make_level_string(loop_var)
    if(sym_tab.symbol_table[search_str] != 'garbage'):
        sub_tree[1][1] = [[str(loop_var), '=', sym_tab.symbol_table[search_str]], ';']
    # print("subtree", sub_tree)

'''custom log fxn'''
def my_log(start, end, factor):
    mi = min(start, end)
    mx = max(start, end)
    start = mi
    end = mx
    count = 0
    while(start < end):
        count += 1
        start *= factor
    return count
