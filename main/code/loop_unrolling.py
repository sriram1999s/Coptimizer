from regenerator import *
from math import *
from symboltable import *
import re


def for_unroll_validate(sub_tree):

    condition = sub_tree[1]
    operators = []
    find_operator(0, len(condition[-2]), condition[-2], operators)
    ids = dict()
    find_id(0, len(condition), condition, ids)
    loop_var = list(ids.keys())[0]
    # print("operators : ", operators)
    solve_substi_id(0,len(condition[1]),condition[1],loop_var)
    solve_expr(0,len(condition),condition)
    
    print("condition: ", condition,"\n")
    
    ids=dict()
    find_id(0, len(condition), condition, ids)
    #print("ids : ",ids)
    if(len(ids) > 1):  # more than 1 loop variable in condition, short circuit return ;;jugaad;;
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
        print("Here")
        return sub_tree


# def substi_id(var):
#     global level_str
#     global symbol_table
#     search_str = var + '_'.join(level_str)
#     if(type(symbol_table[search_str]) == int):
#         return symbol_table[search_str]
#     return 'garbage'

def check_type(l):
    for i in l:
        if(type(i) == list):
            return 0
    return 1
    

def solve_substi_id(i,n,l,loop_var):
    if(i==n):
        return
    if(type(l)==list and (len(l)==3 or len(l)==5) and check_type(l)):
        walk = [0,2]
        if(len(l)==5):
            walk = [1,3] 
        for j in walk:
            if(type(l[j])==str and l[j]!=loop_var):
                search_str = l[j] + '_'.join(level_str)
                if(type(symbol_table[search_str]) == int):
                    l[j] = symbol_table[search_str]	
        
    if(type(l[i])==list and (len(l[i])==3 or len(l[i])==5) and check_type(l[i])):
        walk = [0,2]
        if(len(l[i])==5):
            walk = [1,3] 
        for j in walk:
            if(type(l[i][j])==str and l[i][j]!=loop_var):
                search_str = l[i][j] + '_'.join(level_str)
                if(type(symbol_table[search_str]) == int):
                    l[i][j] = symbol_table[search_str]	
    if(type(l[i])==list):
        for j in l:
            if(type(j)==list):
                solve_substi_id(0,len(j),j,loop_var)
    solve_substi_id(i+1,n,l,loop_var)

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



def for_full_condition(sub_tree, operators, ids):
    condition = sub_tree[1]
    output = []
    type_list = ['int', 'float', 'void', 'double', 'char']

    # if(type(condition[1][0]) != list):  # checking for declaration
    #     if(type(condition[1][3]) == str):  # LHS is variable / expression
    #         # print("Here1-----")
    #         temp = substi_id(condition[1][3])
    #         if(temp != 'garbage'):
    #             condition[1][3] = temp
    #         else:
    #             return sub_tree
    #     elif(type(condition[1][3]) == list):
    #         return sub_tree
    # else:
    #     if(type(condition[1][0][2]) == str):  # LHS is variable / expression
    #         # print("Here2-----")
    #         temp = substi_id(condition[1][0][2])
    #         if(temp != 'garbage'):
    #             condition[1][0][2] = temp
    #         else:
    #             return sub_tree
    #     elif(type(condition[1][0][2]) == list):
    #         return sub_tree

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
            solve(0, len(sub_tree[2]), sub_tree[2], output)
            unrolled = for_full_unroll(output, condition, operators[0][0])
            res = [unrolled]
        else:
            solve(0, len(sub_tree[2]), sub_tree[2], output)
            unrolled = for_partial_unroll(output, condition, operators[0][0])
            res = [sub_tree[0], sub_tree[1], unrolled]
    return res


def for_full_unroll(block, condition, operator):
    print("Unrolling full...\n")
    block.pop(0)
    block.pop()
    # print('operator : ', operator)
    res = []
    # to get start and end value of loop by scanning for integer
    find_int(0, len(condition), condition, res)
    increment_val = 1
    if(len(res) == 3):
        increment_val = res[-1][0]
    if(re.search('[+-]', operator)):
        count_unrolls = int(ceil(abs(res[0][0]-res[1][0])/increment_val))
    else:
        count_unrolls = int(my_log(res[0][0], res[1][0], increment_val))
    return block * count_unrolls


def for_partial_unroll(block, condition, operator):
    print("Unrolling partial...\n")
    block.pop(0)
    block.pop()
    # print(f"operator : {operator}")
    res = []
    increment_val = 1
    find_int(0, len(condition), condition, res)
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

    return ['{']+block*unroll_count+['}'] + block*extra


def find_int(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) is int):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_int(0, len(lis[ind]), lis[ind], res)
    find_int(ind+1, end, lis, res)


def find_operator(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) == str and re.search('[-+*/]', lis[ind])):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_operator(0, len(lis[ind]), lis[ind], res)
    find_operator(ind+1, end, lis, res)


def find_rel_operator(ind, end, lis, res=[]):
    if(ind == end):
        return
    if(type(lis[ind]) == str and re.search('[<>]', lis[ind])):
        res.append([lis[ind], ind])
    elif(type(lis[ind]) is list):
        find_rel_operator(0, len(lis[ind]), lis[ind], res)
    find_rel_operator(ind+1, end, lis, res)


def find_id(ind, end, lis, res=dict()):
    if(ind == end):
        return
    type_list = ['int', 'float', 'void', 'double', 'char']
    if(type(lis[ind]) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', lis[ind]) and lis[ind] not in type_list):
        res[lis[ind]]=0
    elif(type(lis[ind]) is list):
        find_id(0, len(lis[ind]), lis[ind], res)
    find_id(ind+1, end, lis, res)


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
