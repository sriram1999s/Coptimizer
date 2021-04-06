from regenerator import *
from math import *
from symboltable import *
import re
from collections import defaultdict
from copy import deepcopy
#bennur was here
array_hashmap = defaultdict(lambda:[])
array_value = defaultdict(lambda: defaultdict(lambda: 'garbage'))

def make_compile_inits(parse_tree):
    # print(parse_tree)
    for array in array_value:
        if(array_value[array]['value']!='garbage'):
            if(type(array_value[array]['value'])==int):
                rhs = '{'+ (str(array_value[array]['value']) + ',')* (array_value[array]['upper']-1)+ str(array_value[array]['value']) + '}'
            else:
                rhs = array_value[array]['value']
            # print("rhs", rhs)
            # print(array_hashmap[array], rhs)
            # print(parse_tree)
            dec_string = []
            solve(0, len(array_hashmap[array]), array_hashmap[array], dec_string)

            dec_string = ''.join(dec_string)
            new_dec_string = re.sub('([\[\]])', rep ,dec_string)
            parse_tree,c =  re.subn(new_dec_string, dec_string[:-1] + '=' + rhs + ';', parse_tree,flags=re.S)

    return parse_tree

def rep(m):
    return '\\' + m.group(1)
''' adds array to hashmap '''
def add_array(sub_tree):
    # print("sub_tree", sub_tree)
    global level_str
    flag=1
    # for i in range(1,len(sub_tree[2]),3):
    #     if(type(sub_tree[2][i])!=int):
    #         flag=0
    #         break
    if(len(sub_tree[2])==3):
        array_hashmap[sub_tree[1]] = sub_tree

''' checks for possibility of compile time init '''
def compile_init_validate(sub_tree):
    # print("sub_tree", sub_tree)
    # print("\nbody", sub_tree[2])
    condition = sub_tree[1]
    if(condition[1] != ';' and condition[2] != ';' and len(condition) == 5):  # full for condition
        initialize(sub_tree)

def transform(x,val,variation):
    # variation = [variation]
    #print(variation)
    if(type(variation)==int):
        return variation
    if(type(variation)==str):
        return val
    replace_string(0,len(variation),variation,x,val)
    #print("before:",x,val,variation)
    solve_expr(0,len(variation),variation)
    #print("after:",x,val,variation)
    return variation[0]


'''makes series'''
def make_series(lower_limit,upper_limit,loop_var,increment_val,variation='i',lhs_variation='i'):
    #print(f"Series!! {[lower_limit,upper_limit,increment_val,loop_var,variation,lhs_variation]}")
    increment_val = int(increment_val)
    mx=max(lower_limit,upper_limit)
    mi=min(lower_limit,upper_limit)
    ll,ul=lower_limit,upper_limit
    if(lower_limit>upper_limit):
        ll = lower_limit + 1

    space = max(transform(loop_var,ll,deepcopy(lhs_variation))+1,transform(loop_var,ul,deepcopy(lhs_variation)))

    #print("space: ",space)
    res = ['0' for i in range(space)]
    if(lower_limit<upper_limit):
        while(lower_limit<upper_limit):
            lhs,rhs = lhs_variation,variation
            lhs = transform(loop_var,lower_limit,deepcopy(lhs_variation))
            rhs = transform(loop_var,lower_limit,deepcopy(variation))
            #print(f"lhs: {lhs},rhs: {rhs}")
            res[lhs]=str(rhs)
            lower_limit+=1
    else:
        while(lower_limit>upper_limit):
            lhs,rhs = lhs_variation,variation
            lhs = transform(loop_var,lower_limit,deepcopy(lhs_variation))
            rhs = transform(loop_var,lower_limit,deepcopy(variation))
            #print(f"lhs: {lhs},rhs: {rhs}")
            res[lhs]=str(rhs)
            lower_limit-=1

    #res = [str(i) for i in res]
    res = '{' + ','.join(res) + '}'
    return res

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
    if(re.search('^-?[0-9]*$',lower_limit)):
        lower_limit = int(lower_limit)
    m1 = re.search('([<>])(.*?);',''.join(upper_limit_str))
    upper_limit = m1.group(2)
    if(re.search('^-?[0-9]*$',upper_limit)):
        upper_limit = int(upper_limit)

    increment_val = '1'
    #print(''.join(increment_str))
    m2 = re.search('=(.*)',''.join(increment_str))
    if(m2):
        # print(m2.groups())
        increment_val=m2.group(1)

    op = ''
    temp_m = re.search('([+\-\*/])|(\+\+)|(--)',''.join(increment_str))
    if(temp_m):
        if(temp_m.group(1)):
            op = temp_m.group(1)
        elif(temp_m.group(2)):
            op = temp_m.group(2)
        else:
            op = temp_m.group(3)


    #print("increment val:",increment_val)
    series_lowerlimit,series_upperlimit = lower_limit,upper_limit
    if(m1.group(1)=='>'):
        lower_limit,upper_limit = upper_limit,lower_limit
        # print(lower_limit,type(lower_limit))
        if(lower_limit != -1):
            return
    else:
        if(lower_limit != 0):
            return



    #print("lower_limit: ",lower_limit,type(lower_limit))
    #print("upper_limit: ",upper_limit,type(upper_limit))


    ids = dict()
    find_id(0, len(condition[2:]), condition[2:], ids)
    loop_var = list(ids.keys())[0]
    # print("loop_var", loop_var)
    # print(sub_tree[2])
    if(type(lower_limit)==type(upper_limit)==int and increment_val=='1' and op not in ['*','/']):
        find_array(0, len(sub_tree[2]), sub_tree[2], loop_var, series_lowerlimit , series_upperlimit ,op,increment_val)
    # print(sub_tree[2])

''' to find array in body'''
# [['b', '[', 'i', ']'], '=', 0]
# [[['c', '[', 'i', ']'], '=', 1], ';']
def find_array(i, n, l, loop_var, lower,upper,op,inc):
    global level_str
    if(i == n):
        return
    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][0]) == list and len(l[i][0][1])==3 and l[i][1] == '=' and array_value[l[i][0][0]]['value']=='garbage'):
        print("l[i]",l[i])

        if(type(l[i][0][1])==list and l[i][0][1][1]==loop_var):
            if(type(l[i][2]) == int):
                array_value[l[i][0][0]]['value'] = l[i][2]
                array_value[l[i][0][0]]['upper'] = max(lower,upper)
                l[i].clear()
            elif(l[i][2] == loop_var):
                array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc)
                l[i].clear()
            else:
                d = {}
                find_id(0,len(l[i][2]),l[i][2],d)
                if(len(d)>1):
                    return
                array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc,l[i][2])
                l[i].clear()
        else:
            d = {}
            if(type(l[i][2])==list):
                find_id(0,len(l[i][2]),l[i][2],d)
            if(type(l[i][0][1][1])==list):
                find_id(0,len(l[i][0][1][1]),l[i][0][1][1],d)
            if(len(d)>1):
                return
            array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc,l[i][2],l[i][0][1][1])
            l[i].clear()

    if(type(l[i]) == list):
        find_array(0, len(l[i]), l[i], loop_var,lower,upper,op,inc )
    find_array(i+1, n, l,loop_var, lower,upper,op,inc)

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

'''solve_expr'''
def solve_expr(i,n,l):
    if(type(l)==list and len(l)==3 and type(l[0])==int and type(l[1])==str and type(l[2])==int):
        x,y,op=l[0],l[2],l[1]
        l.clear()
        if(op=='+'):
            l.append(x+y)
        elif(op=='-'):
            l.append(x-y)
        elif(op=='*'):
            l.append(x*y)
        elif(op=='/'):
            l.append(x/y)
        elif(op=='&'):
            l.append(x&y)
        elif(op=='|'):
            l.append(x|y)
        elif(op=='^'):
            l.append(x^y)
        elif(op=='<<'):
            l.append(x<<y)
        elif(op=='>>'):
            l.append(x>>y)
        return

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

    elif(type(l[i])==list):
        for j in l:
            if(type(j)==list):
                solve_expr(0,len(j),j)
    solve_expr(i+1,n,l)
