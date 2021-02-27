from regenerator import *
from math import *
import re

def for_unroll_validate(sub_tree, operators, ids):

    print("operators : ", operators)
    print("ids : ", ids)

    condition = sub_tree[1]
    output = []
    print("Printing condition : ", condition)
    # print(sub_tree)
    if(len(ids)>1):
        return sub_tree

    operator_list = ['++', '--','/' ,'*' ,'+' , '-', '+=', '-=', '*=', '/=']
    if(operators[0][0] not in operator_list): # checking for operators
        # print("here")
        return sub_tree

    type_list = ['int', 'float', 'void']
    if(condition[1][0] in type_list): # checking for declaration
        if(type(condition[1][3]) == str or type(condition[1][3]) == list ): # LHS is variable / expression
            # print("Here1-----")
            return sub_tree
    else:
        if(type(condition[1][2]) == str or type(condition[1][2]) == list ): # LHS is variable / expression
            # print("Here2-----")
            return sub_tree

    if(type(condition[2]) == list): # checking for declaration
        ind = 2
    else:
        ind = 3

    if(type(condition[ind][0]) == list or type(condition[ind][2]) == list or type(condition[ind][2]) == str): # LHS or RHS of bounds check is not an expression
        # print("here")
        return sub_tree

    res=[]
    find_int(0,len(condition),condition,res)
    total = abs(res[1][0]-res[0][0])
    
    if(type(condition[ind][2])==int ): # LHS of bounds check is an integer
        if(total <= 35): # full unrolling
            solve(0,len(sub_tree[2]),sub_tree[2],output) #remove nesting in sub_tree[2]
            unrolled = for_full_unroll(output, condition, operators[0][0])
            res = [unrolled]
        else:
            solve(0,len(sub_tree[2]),sub_tree[2],output)
            unrolled = for_partial_unroll(output, condition, operators[0][0])
            res = [sub_tree[0],sub_tree[1],unrolled]
    return res

def for_full_unroll(block, condition, operator):
    block.pop(0)
    block.pop()
    # print('operator : ', operator)
    res=[]
    find_int(0,len(condition),condition,res) # to get start and end value of loop by scanning for integer
    print(res)
    increment_val = 1
    if(len(res) == 3):
        increment_val = res[-1][0]
    if(re.search('[+-]',operator)):
        count_unrolls = int(ceil(abs(res[0][0]-res[1][0])/increment_val))
    else:
        count_unrolls = int(my_log(res[0][0], res[1][0], increment_val))
    return block * count_unrolls

def for_partial_unroll(block, condition, operator):
    block.pop(0)
    block.pop()
    print(f"operator : {operator}")
    res=[]
    increment_val = 1
    find_int(0,len(condition),condition,res)
    print(res)
    total = abs(res[0][0]-res[1][0])
    if(len(res)==3):
        increment_val =  res[-1][0]
    if(re.search('[+-]',operator)):
        count_unrolls = int(ceil(total/increment_val))
    else:
        count_unrolls = int(my_log(res[0][0], res[1][0], increment_val))
    factor = 0.2
    unroll_count = int(count_unrolls*factor)
    condition[2][res[1][-1]] = total//unroll_count + res[0][0] #readjusting the end value of loop after partial unrolling
    extra = total%unroll_count
    return ['{']+block*unroll_count+['}'] + block*extra


def find_int(ind,end,lis,res=[]):
    if(ind==end):
        return
    if(type(lis[ind]) is int):
        res.append([lis[ind],ind])
    elif(type(lis[ind]) is list):
        find_int(0,len(lis[ind]),lis[ind],res)
    find_int(ind+1,end,lis,res)

def find_operator(ind,end,lis, res=[]):
    if(ind==end):
        return
    if(type(lis[ind])==str and re.search('[-+*/]', lis[ind])):
        res.append([lis[ind],ind])
    elif(type(lis[ind]) is list):
        find_operator(0,len(lis[ind]),lis[ind],res)
    find_operator(ind+1,end,lis,res)



def find_id(ind,end,lis, res=set()):
    if(ind==end):
        return
    if(type(lis[ind])==str and re.search('[A-Za-z_][A-Za-z_0-9]*', lis[ind])):
        res.add(lis[ind])
    elif(type(lis[ind]) is list):
        find_id(0,len(lis[ind]),lis[ind],res)
    find_id(ind+1,end,lis,res)

def my_log(start,end,factor):

    mi = min(start, end)
    mx = max(start, end)
    start = mi
    end = mx
    count = 0
    while(start<end):
        count+=1
        start*=factor
    return count
