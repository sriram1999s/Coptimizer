from regenerator import *
from math import *
from symboltable import *
import re
from collections import defaultdict

array_hashmap = defaultdict(lambda:-1)

def add_array(subtree):
    print("subtree: ",subtree)
    if(type(subtree[3])==int):
        array_hashmap[subtree[1]] = subtree[3]


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

