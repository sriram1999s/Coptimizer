from parser import flatten
from collections import defaultdict
class Sentinel:
    def __init__(self):
       self.tagged_data_structures = defaultdict(lambda:None)
       # self.linear_search_bodies = defaultdict(lambda:None)

    '''add data structure to tagged data structure'''
    def add_ds(self,name,statement,type_ds):
        print(f"adding....{name}---->{statement}---->{type_ds}")
        self.tagged_data_structures[name] = [statement,type_ds]
        increase_size_array(statement,type_ds)


    def disp(self):
        for ds in self.tagged_data_structures:
            print(f"{ds}---->{self.tagged_data_structures[ds]}")

    ''' checks if sentinel search is possible '''
    def validate_linear_search(self,sub_tree):
        print("In validate : ", sub_tree)
        self.linear_to_sentinel(sub_tree)

    ''' converts linear search to sentinel search '''
    def linear_to_sentinel(self, sub_tree):
        import re
        if(sub_tree[0] == 'while'):
            bounds_condition = sub_tree[1]
            found_condition, found_body = self.detect_and_remove_if(sub_tree[2])
            # print(f"\n\n linear_to_sentinel : {found_condition}, {found_body}")
            sub_tree[1] = ['(', '!', found_condition , ')']
            found_body_new = re.sub('break\s*?;', '', ''.join(flatten(found_body)))
            # print("fnjhkdv : ", found_body_new, " @ ", ''.join(flatten(found_body)))
            sub_tree.append(['if', bounds_condition, found_body_new])

    # ['while', ['(', ['i', '<', 'n'], ')'], ['{', [['if', ['(', [['a', ['[', 'i', ']']], '==', 'elem'], ')'], ['{', [[['printf', '(', ['"%d.....found"', ',', 'elem'], ')'], ';'], ['break', ';']], '}']], [['i', '++'], ';']], '}']]
    ''' detects the relevant if condition and body '''
    def detect_and_remove_if(self, sub_tree):
        import re
        def check_break(sub_tree):
            flattened_tree = ''.join(flatten(sub_tree))
            if(re.search("break\s*?;", flattened_tree)):
                return True
            return False

        def find(i, n, sub_tree, condition, body):
            if(i == n):
                return
            if(type(sub_tree[i]) == list and sub_tree[i][0] == 'if' and check_break(sub_tree[i][2])):
                condition.append(sub_tree[i][1])
                body.append(sub_tree[i][2])
                sub_tree[i] = []
                return

            if(type(sub_tree[i]) == list):
                find(0 , len(sub_tree[i]), sub_tree[i], condition, body)

            if(type(sub_tree[i]) != list):
                find(i+1 , n, sub_tree, condition, body)


        condition_list = []
        body_list = []
        find(0, len(sub_tree), sub_tree, condition_list, body_list)
        return (condition_list[-1], body_list[-1])

def increase_size_array(statement,type_ds):
    if(type_ds == "array"):
        if(type(statement[2][1]) == int):
            statement[2][1] += 1
        else:
            recursive_insert(0,len(statement[4]),-1,statement[4])

def check_nested(l):
    for sub in l:
        if(type(sub) == list):
            return False
    return True

''' recursively insert dummy val after increasing size '''
def recursive_insert(ind,n,elem,statement):
    if(ind == n):
        return
    if(type(statement[ind]) == list and check_nested(statement[ind]) and len(statement[ind])==3):
        temp = [1,',',1]
        temp[0] = statement[ind][-1]
        temp[-1] = elem
        statement[ind][-1] = temp
        return
    if(type(statement[ind]) == list):
        recursive_insert(0,len(statement[ind]),elem,statement[ind])
    else:
        recursive_insert(ind+1,n,elem,statement)

sentinel = Sentinel()
