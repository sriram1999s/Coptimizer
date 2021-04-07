from collections import defaultdict
import re
class Jamming:
    def __init__(self):
        self._jam_table = defaultdict(lambda: defaultdict(lambda : 'garbage'))
        self._count = 0
    def add(self, lower, upper, inc ,scope, sub_tree):
        body = sub_tree[2]
        self._flag = 0
        self.container = self._jam_table.copy()
        ''' check for similar loops '''
        for loop in self.container:
            self.container = self._jam_table.copy()
            if(self.container[loop]['lower'] == lower and self.container[loop]['upper'] == upper and self.container[loop]['inc'] == inc and self.container[loop]['scope'] == scope):
                self._flag = self.jam(loop, body) # passing loop but not loops body !!!!!!
                if(self._flag):
                    sub_tree[0] = []
                    sub_tree[1] = []
                    sub_tree[2] = []
                    # print("sub_tree : ", sub_tree)
                    self._jam_table[loop]['sub_tree'][2] = ['{'] + self._jam_table[loop]['body'] + ['}']
                    return

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
        # print("here")
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
