from regenerator import *
from math import *
from symboltable import *
import re
from collections import defaultdict

array_hashmap = defaultdict(lambda:[])
array_value = defaultdict(lambda:{})

def make_compile_inits(parse_tree):
    # print(parse_tree)
    for array in array_value:
        rhs = '{'+ (str(array_value[array]['value']) + ',')* (array_value[array]['upper']-1)+ str(array_value[array]['value']) + '}'
        # print("rhs", rhs)
        # print(array_hashmap[array], rhs)
        # print(parse_tree)
        dec_string = []
        solve(0, len(array_hashmap[array]), array_hashmap[array], dec_string)

        dec_string = ''.join(dec_string)
        new_dec_string = re.sub('([\[\]])', rep ,dec_string)
        parse_tree =  re.sub(new_dec_string, dec_string[:-1] + '=' + rhs + ';', parse_tree)
    return parse_tree

def rep(m):
    return '\\' + m.group(1)
''' adds array to hashmap '''
def add_array(sub_tree):
    # print("sub_tree", sub_tree)
    if(type(sub_tree[3])==int):
        array_hashmap[sub_tree[1]] = sub_tree

''' checks for possibility of compile time init '''
def compile_init_validate(sub_tree):
    # print("sub_tree", sub_tree)
    # print("\nbody", sub_tree[2])
    condition = sub_tree[1]
    if(condition[1] != ';' and condition[2] != ';' and len(condition) == 5):  # full for condition
        initialize(sub_tree)


def initialize(sub_tree):
    condition = sub_tree[1]
    lower_limit_str = []
    upper_limit_str = []
    increment_str = []
    solve(0,len(condition[1]),condition[1],lower_limit_str)
    solve(0,len(condition[2]),condition[2],upper_limit_str)
    solve(0,len(condition[3]),condition[3],increment_str)
    m = re.search('=(.*?);',''.join(lower_limit_str))
    lower_limit = m.group(1)
    if(re.search('^[0-9]*$',lower_limit)):
        lower_limit = int(lower_limit)
    m1 = re.search('([<>])(.*?);',''.join(upper_limit_str))
    upper_limit = m1.group(2)
    if(re.search('^[0-9]*$',upper_limit)):
        upper_limit = int(upper_limit)

    increment_val = '1'
    #print(''.join(increment_str))
    m2 = re.search('=(.*)',''.join(increment_str))
    if(m2):
        # print(m2.groups())
        increment_val=m2.group(1)

    # print("increment val:",increment_val)

    if(m1.group(1)=='>'):
        lower_limit,upper_limit = upper_limit,lower_limit

    # print("lower_limit: ",lower_limit,type(lower_limit))
    # print("upper_limit: ",upper_limit,type(upper_limit))
    if(lower_limit != 0):
        return
    

    ids = dict()
    find_id(0, len(condition[2:]), condition[2:], ids)
    loop_var = list(ids.keys())[0]
    # print("loop_var", loop_var)
    find_array(0, len(sub_tree[2]), sub_tree[2], loop_var, upper_limit)
    print(sub_tree[2])

''' to find array in body'''
# [['b', '[', 'i', ']'], '=', 0]
# [[['c', '[', 'i', ']'], '=', 1], ';']
def find_array(i, n, l, loop_var, upper):
    if(i == n):
        return
    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][0]) == list and l[i][1] == '=' and l[i][0][2]==loop_var):
        if(type(l[i][2]) == int):
            array_value[l[i][0][0]]['value'] = l[i][2]
            array_value[l[i][0][0]]['upper'] = upper
            l[i].clear()
    if(type(l[i]) == list):
        find_array(0, len(l[i]), l[i], loop_var, upper)
    find_array(i+1, n, l,loop_var, upper)

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

'''replace_string() ------> given a pat and target substi for target whenever pat is matched in nested iterables'''
def replace_array(i,n,l,pat,target):
    if(i==n):
        return
    if(l[i]==pat):
        print("pat", pat)
        print("target", target)
        l[i][-1]='='
        l[i].append(target)
        l[i].append(';')

    if(type(l[i])==list):
        replace_array(0,len(l[i]),l[i],pat,target)
    replace_array(i+1,n,l,pat,target)


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
