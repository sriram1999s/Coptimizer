from collections import defaultdict
import re
import secrets
import copy
# [x1,y1) , [x2,y2)


def check(x1,y1,x2,y2):
    if(x2<=x1<=y2 or x2<=y1<=y2):
        return 1
                    # [1,3] , [0,4]
    elif(min(x1,y1) > min(x2,y2) and max(x1,y1) < max(x2,y2)):
        return 1

    elif(min(x1,y1) < min(x2,y2) and max(x1,y1) > max(x2,y2)):
        return 1
    return 0

class Jamming:
    def __init__(self):
        self._jam_table = defaultdict(lambda: defaultdict(lambda : 'garbage')) # stores all information of for loops (lower, upper , scope, body, ptr)
        self._count = 0
        self._worst_case = 0
    def add(self, lower, upper, inc ,scope, sub_tree):
        body = sub_tree[2]
        self._flag = 0
        self.container = self._jam_table.copy()
        ''' check for similar loops '''
        for loop in self.container:
            self.container = self._jam_table.copy()
            print("sub_tree ",sub_tree)
            greater_flag = '>' in sub_tree[1][2][0]
            roger_that_jam, ranges, case = self.get_range(loop, lower, upper, inc, scope,greater_flag)
            if(roger_that_jam):
                lower_og = self.container[loop]['lower']
                upper_og = self.container[loop]['upper']
                body_og = self._jam_table[loop]['body']
                sub_tree_2_og = sub_tree[2]
                self._flag = self.jam(loop, body) # passing loop but not loops body !!!!!!
                if(case == 0): # when the ranges are identical
                    if(self._flag):
                        # eliminating
                        sub_tree[0] = []
                        sub_tree[1] = []
                        sub_tree[2] = []
                        # print("sub_tree : ", sub_tree)
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        return

                elif(case == 1): # upper_og != upper else all identical
                    if(self._flag):
                        # declaring variables for min and max ranges
                        min_hash = secrets.token_hex(nbytes=6)
                        max_hash = secrets.token_hex(nbytes=6)
                        min_hash_2 = secrets.token_hex(nbytes=6)
                        declare_min = 'int temp_'+ min_hash + ' = ' + ranges[0] + ';'
                        declare_max = 'int temp_'+ max_hash + ' = ' + ranges[1] + ';'
                        diff = '(' + 'temp_' + max_hash + '-' + 'temp_' + min_hash + ')'
                        declare_min_2 = 'int temp_' + min_hash_2 + ' = ' + f'{diff}<0?{diff}:0' + ';'
                        # eliminating
                        # print(sub_tree[1])
                        #sub_tree[1][2][0][2] = diff
                        replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],upper,'temp_'+min_hash_2)
                        replace_string(0,len(sub_tree[1][1]),sub_tree[1][1],lower,0)
                        #sub_tree[1][1][3] = 0
                        if_block = ['if(' + str('temp_' + max_hash) + '==' + str(self._jam_table[loop]['upper']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree[2] + ['}']
                        sub_tree[2] = ['{'] + if_block + else_block + ['}']
                        # changing first loop
                        self._jam_table[loop]['sub_tree'][1][2][0][2] = 'temp_' + min_hash
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        # adding declare statements at beginning of first loop
                        self._jam_table[loop]['sub_tree'].insert(0,[declare_min] + [declare_max] + [declare_min_2])

                elif(case == 2): # lower_og != lower else all identical
                    if(self._flag):
                        # declaring variables for min and max ranges
                        min_hash = secrets.token_hex(nbytes=6)
                        max_hash = secrets.token_hex(nbytes=6)
                        min_hash_2 = secrets.token_hex(nbytes=6)
                        declare_min = 'int temp_'+ min_hash + ' = ' + ranges[0] + ';'
                        declare_max = 'int temp_'+ max_hash + ' = ' + ranges[1] + ';'
                        diff = '(' + 'temp_' + max_hash + '-' + 'temp_' + min_hash + ')'
                        declare_min_2 = 'int temp_' + min_hash_2 + ' = ' + f'{diff}<{upper}?{diff}:{upper}' + ';'
                        

                        # eliminating
                        # print("dslkvnhioduhv ", sub_tree[1])
                        # sub_tree[1][2][0][2] = diff
                        # sub_tree[1][1][3] = 0
                        replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],upper,'temp_'+min_hash_2)
                        replace_string(0,len(sub_tree[1][1]),sub_tree[1][1],lower,0)
                        
                        if_block = ['if(' + str('temp_' + min_hash) + '==' + str(self._jam_table[loop]['lower']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree[2] + ['}']
                        sub_tree[2] = ['{'] + if_block + else_block + ['}']

                        # changing first loop
                        self._jam_table[loop]['sub_tree'][1][1][3] = 'temp_' + max_hash
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        # adding declare statements at beginning of first loop
                        self._jam_table[loop]['sub_tree'].insert(0,[declare_min] + [declare_max] + [declare_min_2])

                elif(case == 3): # worst case upper and lower not equal
                    print("\n\nin case 3 : ", sub_tree)
                    print("\n\nin case 3 : ", self.container[loop]['sub_tree'])

                    temp_tree_1 = copy.deepcopy(sub_tree)
                    temp_tree_2 = copy.deepcopy(self.container[loop]['sub_tree'])
                    self._worst_case = 1
                    if(self._flag):
                        # declaring variables for min and max ranges
                        min_lower_hash = secrets.token_hex(nbytes=6)
                        max_lower_hash = secrets.token_hex(nbytes=6)
                        min_upper_hash = secrets.token_hex(nbytes=6)
                        max_upper_hash = secrets.token_hex(nbytes=6)
                        lower_og = self.container[loop]['lower']
                        upper_og = self.container[loop]['upper']
                        if(greater_flag):
                            if_cond = f"if(check_overlap({lower}+1, {upper}+1, {lower_og}, {upper_og}))"
                        else:
                            if_cond = f"if(check_overlap({lower}, {upper}, {lower_og}, {upper_og}))"
                        declare_min = if_cond + '{\n' + 'int temp_'+ min_lower_hash + ' = ' + ranges[0] + ';' + 'int temp_'+ min_upper_hash + ' = ' + ranges[2] + ';'
                        declare_max = 'int temp_'+ max_lower_hash + ' = ' + ranges[1] + ';' + 'int temp_'+ max_upper_hash + ' = ' + ranges[3] + ';'
                        diff_lower = '(' + 'temp_' + max_lower_hash + '-' + 'temp_' + min_lower_hash + ')'
                        diff_upper = '(' + 'temp_' + max_upper_hash + '-' + 'temp_' + min_upper_hash + ')'
                        #
                        print("dslkvnhioduhv ", sub_tree[1][1] , lower)
                        # replacing second loop with remaining part of lower range
                        # sub_tree[1][2][0][2] = diff_lower
                        # sub_tree[1][1][3] = 0
                        
                        if(greater_flag):
                            replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],lower,diff_lower)
                            replace_string(0,len(sub_tree[1][1]),sub_tree[1][1],upper,0)
                            replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],'>','<')
                            replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'--','++')
                            replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'-=','+=')
                            replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'-','+')
                            # semicolon_index = declare_max.index(';')
                            # declare_max = declare_max[0:semicolon_index] + '+ 1' + declare_max[semicolon_index:]
                        else:
                            replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],upper,diff_lower)
                            replace_string(0,len(sub_tree[1][1]),sub_tree[1][1],lower,0)
                            
                        if_block = ['if(' + str('temp_' + min_lower_hash) + '==' + str(self._jam_table[loop]['lower']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree_2_og + ['}']
                        sub_tree[2] = ['{'] + if_block + else_block + ['}']

                        # changing first loop ------> intersected loop [common range]
                        self._jam_table[loop]['sub_tree'][1][1][3] = 'temp_' + max_lower_hash
                        self._jam_table[loop]['sub_tree'][1][2][0][2] = 'temp_' + min_upper_hash
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        # adding declare statements at beginning of first loop
                        self._jam_table[loop]['sub_tree'].insert(0,[declare_min] + [declare_max])

                        # creating another loop to cover remaining part of upper range
                        if_block = ['if(' + str('temp_' + max_upper_hash) + '==' + str(self._jam_table[loop]['upper']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree_2_og + ['}']
                        body = ['{'] + if_block + else_block + ['}']
                        extra_for = ['for(int z = 0 ; z < ' + diff_upper + ';z++)'] + body + ['}']

                        else_condition = ['else {'] + temp_tree_1 + temp_tree_2 + ['}']
                        final = extra_for + else_condition
                        # adding this list to parse tree in sub_tree
                        # sub_tree.append(extra_for)
                        sub_tree.append(final)



        ''' if jamming not possible , add to jam_table '''
        if(not self._flag):
            temp = 'for' + str(self._count)
            if('>' in sub_tree[1][2][0]):
                self._jam_table[temp]['lower'] = str(lower) + '+1'
            else:
                self._jam_table[temp]['lower'] = lower
            if('>' in sub_tree[1][2][0]):
                self._jam_table[temp]['upper'] = str(upper) + '+1'
                replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],lower,self._jam_table[temp]['upper'])
                replace_string(0,len(sub_tree[1][1]),sub_tree[1][1],upper,self._jam_table[temp]['lower'])
                replace_string(0,len(sub_tree[1][2]),sub_tree[1][2],'>','<')
                replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'--','++')
                replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'-=','+=')
                replace_string(0,len(sub_tree[1][3]),sub_tree[1][3],'-','+')
            else:
                self._jam_table[temp]['upper'] = upper
            self._jam_table[temp]['inc'] = inc
            self._jam_table[temp]['scope'] = scope
            self._jam_table[temp]['body'] = body
            self._jam_table[temp]['sub_tree'] = sub_tree
            self._count += 1

    ''' checks for jamming possibility '''
    # 1. check if var are modified anywhere between the loops
    # 2. var in second loop depends on value after first loop exec
    def check_jam(self, loop, body_to_jam):
        self._ret =  check_intersect(self._jam_table[loop]["body"], body_to_jam)
        return self._ret

    ''' jams two loops if possible '''
    def jam(self, loop, body_to_jam):
        self.possible = self.check_jam(loop, body_to_jam)
        if(not self.possible):
            return 0

        self._jam_table[loop]["body"] = self._jam_table[loop]["body"] + body_to_jam
        return 1

    ''' display function '''
    def disp(self):
        # print(self._jam_table)
        for loop in self._jam_table.copy():
            print(f"{loop} ----> {self._jam_table[loop]['lower']}")
            print(f"     ----> {self._jam_table[loop]['upper']}")
            print(f"     ----> {self._jam_table[loop]['inc']}")
            print(f"     ----> {self._jam_table[loop]['scope']}")
            print(f"     ----> {self._jam_table[loop]['body']}")
            print(f"     ----> {self._jam_table[loop]['sub_tree']}")

    ''' check for range equality '''
    def get_range(self, loop, lower, upper, inc, scope,greater_flag):
        lower_og = self.container[loop]['lower']
        upper_og = self.container[loop]['upper']
        inc_og = self.container[loop]['inc']
        scope_og = self.container[loop]['scope']

        if(abs(int(inc_og)) == abs(int(inc)) and scope_og == scope):
            min_range, max_range = 0, 0
            if(lower == lower_og and upper == upper_og):
                return (True, [lower, upper], 0)
            # when lower  ==  lower_og and upper differs Case 1
            elif(lower == lower_og):
                if(type(upper) == str or type(upper_og) == str):
                    upper, upper_og = str(upper), str(upper_og)
                    min_range = '(' + upper + '<' + upper_og +'?' + upper + ':' + upper_og + ')'
                    max_range = '(' + upper + '>' + upper_og +'?' + upper + ':' + upper_og + ')'
                    diff = max_range + ' - ' + min_range
                else:
                    min_range = min(upper, upper_og)
                    max_range = max(upper, upper_og)
                    diff = max_range - min_range

                return (True, [min_range, max_range, diff], 1)
            # when upper == upper_og and lower differs Case 2
            elif(upper == upper_og):
                if(type(lower) == str or type(lower_og) == str):
                    upper, upper_og = str(upper), str(upper_og)
                    min_range = '(' + lower + '<' + lower_og +'?' + lower + ':' + lower_og + ')'
                    max_range = '(' + lower + '>' + lower_og +'?' + lower + ':' + lower_og + ')'
                    diff = max_range + ' - ' + min_range
                else:
                    min_range = str(min(lower, lower_og))
                    max_range = str(max(lower, lower_og))
                    diff = int(max_range) - int(min_range)
                return (True, [min_range, max_range, diff], 2)
            # when both differ worst case scenarion consider these 2 intervals [0,n],[n/2,2n] Case 3
            else:

                if(type(lower)==str or type(lower_og)==str):
                    lower, lower_og = str(lower), str(lower_og)
                    if(greater_flag):
                        lower = lower + '+1'
                    min_lower_lower_og = '(' + lower + '<' + lower_og +'?' + lower + ':' + lower_og + ')'
                    max_lower_lower_og = '(' + lower + '>' + lower_og +'?' + lower + ':' + lower_og + ')'
                else:
                    if(greater_flag):
                        lower = lower+1
                    min_lower_lower_og = str(min(lower,lower_og))
                    max_lower_lower_og = str(max(lower,lower_og))

                if(type(upper)==str or type(upper_og)==str):
                    upper, upper_og = str(upper), str(upper_og)
                    if(greater_flag):
                        upper = upper + '+1'
                    min_upper_upper_og = '(' + upper + '<' + upper_og +'?' + upper + ':' + upper_og + ')'
                    max_upper_upper_og = '(' + upper + '>' + upper_og +'?' + upper + ':' + upper_og + ')'
                else:
                    if(greater_flag):
                        upper = upper + 1 
                    min_upper_upper_og = str(min(upper,upper_og))
                    max_upper_upper_og = str(max(upper,upper_og))

                diff_lower = 0
                diff_upper = 0
                return (True,[min_lower_lower_og,max_lower_lower_og,min_upper_upper_og,max_upper_upper_og,diff_lower,diff_upper],3)


        return (False,[],-1)

#------------------------------------class ends-----------------------------------------


''' checks for intersection of variables between 2 bodies'''
def check_intersect(body1, body2):
    # id1 = {}
    # id2 = {}
    # find_id(0, len(body1), body1, id1)
    # find_id(0, len(body2), body2, id2)

    # id1 = set(id1.keys())
    # id2 = set(id2.keys())
    # inter = id1&id2

    left_side_body1 = find_lhs_id(0,len(body1),body1)
    left_side_body2 = find_lhs_id(0,len(body2),body2)
    right_side_body1 = find_rhs_id(0,len(body1),body1)
    right_side_body2 = find_rhs_id(0,len(body2),body2)

    print(f"left_side_body 1 : {left_side_body1}")
    print(f"left_side_body 2 : {left_side_body2}")
    print(f"right_side_body 1 : {right_side_body1}")
    print(f"right_side_body 2 : {right_side_body2}")

    inter1 = set(left_side_body1) & set(right_side_body2)
    inter2 = set(left_side_body2) & set(right_side_body1)

    print("Inter l1 - r2 : ",inter1)
    print("Inter r1 - l2 : ",inter2)

    if(inter1 or inter2):
        return 0
    return 1

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

'''find_lhs_id() ------> scans for variables on lhs of '=' '''
def find_lhs_id(ind,end,lis):
    if(ind==end):
        return []
    elif(type(lis[ind])==list and len(lis[ind])==3 and re.search(r'=',lis[ind][1])):
        return [''.join(lis[ind][0])]+find_lhs_id(ind+1,end,lis)
    elif(type(lis[ind])==list and len(lis[ind])==2 and check_list(lis[ind])):
        res = []
        for var in lis[ind]:
            if(var not in ['++','--']):
                res.append(var)
        return res + find_lhs_id(ind+1,end,lis)
            
    elif(type(lis[ind])==list):
        return find_lhs_id(0,len(lis[ind]),lis[ind]) + find_lhs_id(ind+1,end,lis)
    else:
        return find_lhs_id(ind+1,end,lis)
        

'''find_lhs_id() ------> scans for variables on rhs of '=' '''
def find_rhs_id(ind,end,lis):
    if(ind==end):
        return []
    if(type(lis[ind])==list and len(lis[ind])==3 and re.search(r'=',lis[ind][1])):
        res = []
        for var in flatten(lis[ind][2]):
            if(re.search('[A-Za-z_][A-Za-z_0-9]*',str(var))):
                res.append(var)
        lhs_var = ''.join(lis[ind][0])
        if(lhs_var in res):
            res.remove(lhs_var)
        res = list(set(res))
        return res+find_rhs_id(ind+1,end,lis)
    elif(type(lis[ind])==list):
        return find_rhs_id(0,len(lis[ind]),lis[ind]) + find_rhs_id(ind+1,end,lis)
    else:
        return find_rhs_id(ind+1,end,lis)
    
       

''' generate check_overlap_function '''
def gen_check(worst_case):
    final_condition = ''
    if(worst_case):
        ''' have to change this later '''
        # fn_hash = secrets.token_hex(nbytes=6
        fn_hash = ''

        fn_dec = 'int' + ' check_overlap' + fn_hash + '(int x1, int y1, int x2, int y2) {'

        return_1 = 'return 1;'
        return_0 = 'return 0;'

        zero_condition = 'if(x1>y1 || x2>y2)' + return_0

        first_condition = 'if((x1>=x2 && x1<y2) || (y1>x2 && y1<=y2) || '
        second_condition = '((x1<y1?x1:y1) > (x2<y2?x2:y2) && (x1>y1?x1:y1) < (x2>y2?x2:y2)) ||'
        third_condition = '((x1<y1?x1:y1) < (x2<y2?x2:y2) && (x1>y1?x1:y1) > (x2>y2?x2:y2)))'

        final_condition = fn_dec + zero_condition + first_condition + second_condition + third_condition + return_1 + return_0 + '}';
    return final_condition


'''replace_string() ------> given a pat and target substi for target whenever pat is matched in nested iterables'''
def replace_string(i,n,l,pat,target):
    if(i==n):
        return
    if(type(l[i])==list and check_list(l[i])):
        #print("louda",pat,''.join([str(j) for j in l[i]]).strip())
        if(pat == ''.join([str(j) for j in l[i]]).strip()): 
            l[i]=target
    if(l[i]==pat):
        l[i] = target
    if(type(l[i])==list):
        replace_string(0,len(l[i]),l[i],pat,target)
    replace_string(i+1,n,l,pat,target)


'''check whether type of variable is list (helper fxn)'''
def check_list(l):
    for i in l:
        if(type(i) == list):
            return 0
    return 1

'''flatten list'''
def flatten(L):
    for l in L:
        if isinstance(l, list):
            yield from flatten(l)
        else:
            yield l


''' Jamming object'''
jam = Jamming()
