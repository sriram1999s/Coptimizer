from collections import defaultdict
import re
import secrets


class Jamming:
    def __init__(self):
        self._jam_table = defaultdict(lambda: defaultdict(lambda : 'garbage')) # stores all information of for loops (lower, upper , scope, body, ptr)
        self._count = 0
    def add(self, lower, upper, inc ,scope, sub_tree):
        body = sub_tree[2]
        self._flag = 0
        self.container = self._jam_table.copy()
        ''' check for similar loops '''
        for loop in self.container:
            self.container = self._jam_table.copy()

            roger_that_jam, ranges, case = self.get_range(loop, lower, upper, inc, scope)
            if(roger_that_jam):
                body_og = self._jam_table[loop]['body']
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
                        declare_min = 'int temp_'+ min_hash + ' = ' + ranges[0] + ';'
                        declare_max = 'int temp_'+ max_hash + ' = ' + ranges[1] + ';'
                        diff = '(' + 'temp_' + max_hash + '-' + 'temp_' + min_hash + ')'
                        # eliminating
                        sub_tree[1][2][0][2] = diff 
                        sub_tree[1][1][3] = 0
                        if_block = ['if(' + str('temp_' + max_hash) + '==' + str(self._jam_table[loop]['upper']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree[2] + ['}']
                        sub_tree[2] = ['{'] + if_block + else_block + ['}']
                        # changing first loop
                        self._jam_table[loop]['sub_tree'][1][2][0][2] = 'temp_' + min_hash
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        self._jam_table[loop]['sub_tree'].insert(0,[declare_min] + [declare_max])
                        
                elif(case == 2): # lower_og != lower else all identical
                    if(self._flag):
                        # declaring variables for min and max ranges
                        min_hash = secrets.token_hex(nbytes=6)
                        max_hash = secrets.token_hex(nbytes=6)
                        declare_min = 'int temp_'+ min_hash + ' = ' + ranges[0] + ';'
                        declare_max = 'int temp_'+ max_hash + ' = ' + ranges[1] + ';'
                        diff = '(' + 'temp_' + max_hash + '-' + 'temp_' + min_hash + ')'
                        
                        # eliminating
                        # print("dslkvnhioduhv ", sub_tree[1])
                        sub_tree[1][2][0][2] = diff
                        sub_tree[1][1][3] = 0
                        if_block = ['if(' + str('temp_' + min_hash) + '==' + str(self._jam_table[loop]['lower']) + ')'] + ['{'] + body_og + ['}']
                        else_block = ['else' + '{'] + sub_tree[2] + ['}']
                        sub_tree[2] = ['{'] + if_block + else_block + ['}']

                        # changing first loop
                        self._jam_table[loop]['sub_tree'][1][1][3] = 'temp_' + max_hash
                        self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                        self._jam_table[loop]['sub_tree'].insert(0,[declare_min] + [declare_max])

        ''' if jamming not possible , add to jam_table '''
        if(not self._flag):
            temp = 'for' + str(self._count)
            self._jam_table[temp]['lower'] = lower
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
    def get_range(self, loop, lower, upper, inc, scope):
        lower_og = self.container[loop]['lower']
        upper_og = self.container[loop]['upper']
        inc_og = self.container[loop]['inc']
        scope_og = self.container[loop]['scope']

        if(abs(int(inc_og)) == abs(int(inc)) and scope_og == scope):
            min_range, max_range = 0, 0
            if(lower == lower_og and upper == upper_og):
                return (True, [lower, upper], 0)
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
            elif(upper == upper_og):
                if(type(lower) == str or type(lower_og) == str):
                    min_range = '(' + lower + '<' + lower_og +'?' + lower + ':' + lower_og + ')'
                    max_range = '(' + lower + '>' + lower_og +'?' + lower + ':' + lower_og + ')'
                    diff = max_range + ' - ' + min_range
                else:
                    min_range = min(lower, lower_og)
                    max_range = max(lower, lower_og)
                    diff = max_range - min_range

                return (True, [min_range, max_range, diff], 2)
        return (False,[],-1)

#------------------------------------class ends-----------------------------------------


''' checks for intersection of variables between 2 bodies'''
def check_intersect(body1, body2):
    id1 = {}
    id2 = {}
    find_id(0, len(body1), body1, id1)
    find_id(0, len(body2), body2, id2)

    id1 = set(id1.keys())
    id2 = set(id2.keys())
    inter = id1&id2
    # print(inter)
    if len(inter):
        return 0
    else:
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

''' Jamming object'''
jam = Jamming()
