from regenerator import *
from math import *
from symboltable import *
import re
from collections import defaultdict
from copy import deepcopy



class CompileInit:
    def __init__(self):
        ''' stores all array information '''
        self.array_hashmap = defaultdict(lambda:[])
        ''' stores array range information '''
        self.array_value = defaultdict(lambda: defaultdict(lambda: 'garbage'))

    ''' adds array to hashmap '''
    def add_array(self,OPTIMIZE,sub_tree):
        global level_str
        if(not OPTIMIZE):
            return
        if(len(sub_tree[2])==3):
            self.array_hashmap[sub_tree[1]] = sub_tree

    ''' checks for possibility of compile time init '''
    def compile_init_validate(self,OPTIMIZE,sub_tree):
        if(not OPTIMIZE):
            return
        self.condition = sub_tree[1]
        if(self.condition[1] != ';' and self.condition[2] != ';' and len(self.condition) == 5):  # full for condition
            self.initialize(sub_tree)

    ''' adds meta data for conpile time initialization at controller ''' 
    def initialize(self, sub_tree):
        self.condition = sub_tree[1]
        self.lower_limit_str = []
        self.upper_limit_str = []
        self.increment_str = []
        self.lower_limit_str = solve(0,len(self.condition[1]),self.condition[1])
        self.upper_limit_str = solve(0,len(self.condition[2]),self.condition[2])
        self.increment_str = solve(0,len(self.condition[3]),self.condition[3])
        self.m = re.search('=(.*?);',''.join(self.lower_limit_str))
        self.lower_limit = self.m.group(1)
        if(re.search('^-?[0-9]*$',self.lower_limit)):
            self.lower_limit = int(self.lower_limit)
        self.m1 = re.search('([<>])(.*?);',''.join(self.upper_limit_str))
        self.upper_limit = self.m1.group(2)
        if(re.search('^-?[0-9]*$',self.upper_limit)):
            self.upper_limit = int(self.upper_limit)

        self.increment_val = '1'
        self.m2 = re.search('=(.*)',''.join(self.increment_str))
        if(self.m2):
            self.increment_val= self.m2.group(1)

        self.op = ''
        self.temp_m = re.search('([+\-\*/])|(\+\+)|(--)',''.join(self.increment_str))
        if(self.temp_m):
            if(self.temp_m.group(1)):
                self.op = self.temp_m.group(1)
            elif(self.temp_m.group(2)):
                self.op = self.temp_m.group(2)
            else:
                self.op = self.temp_m.group(3)


        self.series_lowerlimit,self.series_upperlimit = self.lower_limit,self.upper_limit
        if(self.m1.group(1)=='>'):
            self.lower_limit,self.upper_limit = self.upper_limit,self.lower_limit
            if(self.lower_limit != -1):
                return
        else:
            if(self.lower_limit != 0):
                return
        self.ids = dict()
        find_id(0, len(self.condition[2:]), self.condition[2:], self.ids)
        self.loop_var = list(self.ids.keys())[0]
        if(type(self.lower_limit)==type(self.upper_limit)==int and self.increment_val=='1' and self.op not in ['*','/']):

            self.find_array(0, len(sub_tree[2]), sub_tree[2], self.loop_var, self.series_lowerlimit , self.series_upperlimit ,self.op,self.increment_val)

    ''' to find array in body'''
    # [['b', '[', 'i', ']'], '=', 0]
    # [[['c', '[', 'i', ']'], '=', 1], ';']
    def find_array(self, i, n, l, loop_var, lower,upper,op,inc):
        global level_str
        if(i == n):
            return
        if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][0]) == list and len(l[i][0][1])==3 and l[i][1] == '=' and self.array_value[l[i][0][0]]['value']=='garbage'):
            if(type(l[i][0][1])==list and l[i][0][1][1]==loop_var):
                if(type(l[i][2]) == int):
                    self.array_value[l[i][0][0]]['value'] = l[i][2]
                    self.array_value[l[i][0][0]]['upper'] = max(lower,upper)
                    l[i].clear()
                elif(l[i][2] == loop_var):
                    self.array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc)
                    l[i].clear()
                else:
                    d = {}
                    find_id(0,len(l[i][2]),l[i][2],d)
                    if(len(d)>1):
                        return
                    self.array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc,l[i][2])
                    l[i].clear()
            else:
                d = {}
                if(type(l[i][2])==list):
                    find_id(0,len(l[i][2]),l[i][2],d)
                if(type(l[i][0][1][1])==list):
                    find_id(0,len(l[i][0][1][1]),l[i][0][1][1],d)
                if(len(d)>1):
                    return
                self.array_value[l[i][0][0]]['value'] = make_series(lower,upper,loop_var,inc,l[i][2],l[i][0][1][1])
                l[i].clear()

        if(type(l[i]) == list):
            self.find_array(0, len(l[i]), l[i], loop_var,lower,upper,op,inc )
        self.find_array(i+1, n, l,loop_var, lower,upper,op,inc)



    ''' final substitutions done in this fn'''
    def make_compile_inits(self,OPTIMIZE,parse_tree):
        if(not OPTIMIZE):
            return parse_tree
        for array in self.array_value:
            if(self.array_value[array]['value']!='garbage'):
                if(type(self.array_value[array]['value'])==int):
                    self.rhs = '{'+ (str(self.array_value[array]['value']) + ',')* (self.array_value[array]['upper']-1)+ str(self.array_value[array]['value']) + '}'
                else:
                    self.rhs = self.array_value[array]['value']
                self.dec_string = []
                self.dec_string = solve(0, len(self.array_hashmap[array]), self.array_hashmap[array])
                self.dec_string = ''.join(self.dec_string)
                self.new_dec_string = re.sub('([\[\]])', rep ,self.dec_string)
                parse_tree,self.c =  re.subn(self.new_dec_string, self.dec_string[:-1] + '=' + self.rhs + ';', parse_tree,flags=re.S)
        return parse_tree

    def disp(self):
        print('printing array hashmap....')
        for i in self.array_hashmap:
            if(self.array_hashmap[i]!=-1):
                print(f'\t{i}-------->{self.array_hashmap[i]}')

        print('printing array values....')
        for i in self.array_value:
            if(self.array_value[i]!=-1):
                print(f'\t{i}-------->{self.array_value[i]}')

#----------------------------------------------------------helper fns begin ---------------------------------------------
def rep(m):
    return '\\' + m.group(1)

''' calculates according to variation '''
def transform(x,val,variation):
    if(type(variation)==int):
        return variation
    if(type(variation)==str):
        return val
    replace_string(0,len(variation),variation,x,val)
    solve_expr(0,len(variation),variation)
    return variation[0]


'''generates the series for initializing '''
def make_series(lower_limit,upper_limit,loop_var,increment_val,variation='i',lhs_variation='i'):
    increment_val = int(increment_val)
    mx=max(lower_limit,upper_limit)
    mi=min(lower_limit,upper_limit)
    ll,ul=lower_limit,upper_limit
    if(lower_limit>upper_limit):
        ll = lower_limit + 1

    space = max(transform(loop_var,ll,deepcopy(lhs_variation))+1,transform(loop_var,ul,deepcopy(lhs_variation)))
    res = ['0' for i in range(space)]
    if(lower_limit<upper_limit):
        while(lower_limit<upper_limit):
            lhs,rhs = lhs_variation,variation
            lhs = transform(loop_var,lower_limit,deepcopy(lhs_variation))
            rhs = transform(loop_var,lower_limit,deepcopy(variation))
            res[lhs]=str(rhs)
            lower_limit+=1
    else:
        while(lower_limit>upper_limit):
            lhs,rhs = lhs_variation,variation
            lhs = transform(loop_var,lower_limit,deepcopy(lhs_variation))
            rhs = transform(loop_var,lower_limit,deepcopy(variation))
            res[lhs]=str(rhs)
            lower_limit-=1

    res = '{' + ','.join(res) + '}'
    return res



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

'''a function to solve expressions '''
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

#defining com_init global object
com_init = CompileInit()
