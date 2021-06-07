from collections import defaultdict
import re

class SymbolTable:
    def __init__(self):
        self.symbol_table = defaultdict(lambda:'garbage')
        self.level = '%'
        self.level_str = []

    def make_level_string(self,var):
        self.copy_level_str = self.level_str.copy()
        self.search_string = str(var) + ''.join(self.copy_level_str)
        while(self.symbol_table[self.search_string]=='garbage' and len(self.copy_level_str)>1):
            self.copy_level_str.pop()
            self.search_string = str(var) + ''.join(self.copy_level_str)
        return self.search_string

    def lookahead(self,i,n,l):
        if(i == n):
            return

        if(type(l[i]) == list):
            self.flag = True
            if(check_type(l[i]) == 0):
                self.flag = False
            if(self.flag):
                self.id = ''
                self.change = False
                if(len(l[i])==2):
                    for k in l[i]:
                        if(type(k) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', k)):
                            self.id = k;
                            self.change = True
                else:
                    self.ind_id = 0
                    self.op_ind = 0
                    self.f = False
                    for k in l[i]:
                        if(type(k) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', k)):
                            if(self.f == False):
                                self.id = k
                                self.change = True
                                break
                        if(type(k) == str and re.search('[^<>!=]?=', k)):
                            self.f = True
                if(self.change):
                    self.search_str = self.make_level_string(self.id)
                    self.pointer_search_str = self.make_level_string('*'+self.id)

                    if(self.symbol_table[self.pointer_search_str]!='garbage' and type(self.symbol_table[self.pointer_search_str])==str):
                        self.rhs_search_str = self.make_level_string(self.symbol_table[self.pointer_search_str])
                        if(self.symbol_table[self.rhs_search_str]!= 'garbage'):
                            self.symbol_table[self.rhs_search_str] = 'declared'

                    if(self.symbol_table[self.search_str]!= 'garbage'):
                        self.symbol_table[self.search_str] = 'declared'
            else:
                self.lookahead(0, len(l[i]), l[i])

        self.lookahead(i + 1, len(l), l)

    def disp(self):
        for i in self.symbol_table:
            if(self.symbol_table[i] != 'garbage'):
                print(f"\t{i}------->{self.symbol_table[i]}")

#=============================================================================helper========================================================================================#


'''check whether type of variable is list (helper fxn)'''
def check_type(l):
    for i in l:
        if(type(i) == list):
            return 0
    return 1

#defining symboltable global object
sym_tab = SymbolTable()
