from parser import flatten
from collections import defaultdict
import secrets

class Sentinel:
    def __init__(self):
       self.tagged_data_structures = defaultdict(lambda:None)
       # self.linear_search_bodies = defaultdict(lambda:None)

    '''add data structure to tagged data structure'''
    def add_ds(self,name,statement,type_ds):
        print(f"adding....{name}---->{statement}---->{type_ds}")
        self.tagged_data_structures[name] = [statement,type_ds]
        # increase_size_array(statement,type_ds)


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
            found_condition_raw, found_body = self.detect_and_remove_if(sub_tree[2])

            # chain multiple conditions using ||
            found_condition_formatted = []
            for condition in found_condition_raw:
                found_condition_formatted.append(''.join([str(j) for j in flatten(condition)]))
                
            found_condition = ' || '.join(found_condition_formatted)
            # print(f"\n\n linear_to_sentinel : {found_condition}, {found_body}")
            sub_tree[1] = ['(', '!', '(', found_condition, ')', ')']

            found_body_new = []
            for body in found_body:
                found_body_new.append(re.sub(r'break\s*?;', '', ''.join(flatten(body))))
            # print("fnjhkdv : ", found_body_new, " @ ", ''.join(flatten(found_body)))
            insert_code, name, hash = self.add_sentinel(found_condition_raw[0])
            print("\n\ninsert code : ", insert_code)
            bounds_condition.insert(-1, '-')
            bounds_condition.insert(-1, '1')
            sub_tree.append(['if(', bounds_condition, f'|| ({name}[n{hash} -1] == temp{hash}))', ''.join(found_body_new)])
            sub_tree.insert(0, insert_code)

    # ['while', ['(', ['i', '<', 'n'], ')'], ['{', [['if', ['(', [['a', ['[', 'i', ']']], '==', 'elem'], ')'], ['{', [[['printf', '(', ['"%d.....found"', ',', 'elem'], ')'], ';'], ['break', ';']], '}']], [['i', '++'], ';']], '}']]
    ''' detects the relevant if condition and body '''
    def detect_and_remove_if(self, sub_tree):
        import re
        def check_break(sub_tree):
            flattened_tree = ''.join(flatten(sub_tree))
            if(re.search(r"break\s*?;", flattened_tree)):
                return True
            return False

        def check_instructions(sub_tree):
            flattened_list = flatten(sub_tree)
            for elem in flattened_list:
                # print(elem)
                if(re.search("[-+*/=]", str(elem))):
                    return False
            return True

        def find(i, n, sub_tree, condition, body):
            if(i == n):
                return
            if(type(sub_tree[i]) == list and sub_tree[i][0] == 'if' and check_break(sub_tree[i][2]) and check_instructions(sub_tree[i][2])):
                # print("asdasd ",sub_tree[i][1])
                condition.append(sub_tree[i][1])
                body.append(sub_tree[i][2])
                sub_tree[i] = []

            if(type(sub_tree[i]) == list):
                find(0, len(sub_tree[i]), sub_tree[i], condition,body)

            find(i+1, n, sub_tree, condition, body)

        condition_list = []
        body_list = []
        find(0, len(sub_tree), sub_tree, condition_list, body_list)
        return (condition_list, body_list[-1])

    ''' adds sentinel value to end of tagged ds '''
    def add_sentinel(self, condition):
        import re
        flattened_condition = ''.join(flatten(condition))
        flattened_condition = re.sub(r"\(", r" ( ", flattened_condition)
        flattened_condition = re.sub(r"\)", r" ) ", flattened_condition)
        pat = r"\s([^()]*?)\["
        m = re.search(pat, flattened_condition)
        name = ''
        if(m):
            name = m.group(1)

        pat = r"==\s*(.*?)\s"
        m = re.search(pat, flattened_condition)
        sentinel = ''
        if(m):
            sentinel = m.group(1)

        # print("name, sentinel : ", name, sentinel)
        hash = secrets.token_hex(nbytes=4)
        code = f"int n{hash} = sizeof({name}) / sizeof(int);"
        code += f"int temp{hash} = {name}[n{hash} - 1];"
        code += f" {name}[n{hash} - 1] = {sentinel};"
        return code, name, hash


def increase_size_array(statement,type_ds):
    if(type_ds == "array"):
        if(type(statement[2][1]) == int):
            statement[2][1] += 1
        else:
            recursive_insert(0, len(statement[4]), -1, statement[4])

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
        temp = [1, ',', 1]
        temp[0] = statement[ind][-1]
        temp[-1] = elem
        statement[ind][-1] = temp
        return
    if(type(statement[ind]) == list):
        recursive_insert(0, len(statement[ind]), elem, statement[ind])
    else:
        recursive_insert(ind+1, n, elem, statement)

sentinel = Sentinel()
