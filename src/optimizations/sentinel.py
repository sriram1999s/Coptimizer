from parser import flatten
from collections import defaultdict
from optimizations.equation_solver import equation_solve
import secrets

class Sentinel:
    def __init__(self):
       self.tagged_data_structures = defaultdict(lambda:None)
       self.predicates = defaultdict(lambda:None)
       self.salt = '_' + secrets.token_hex(nbytes=4)
       self.change_pred = True
       # self.linear_search_bodies = defaultdict(lambda:None)

    '''add data structure to tagged data structure'''
    def add_ds(self,name,statement,type_ds):
        print(f"adding....{name}---->{statement}---->{type_ds}")
        self.tagged_data_structures[name] = [statement, type_ds]
        # increase_size_array(statement,type_ds)

    '''
    ['int', 'predicate', '(', ['int', 'a'], ')', [['{', [[['if', ['(', ['a', '&', 1], ')'], ['{', [[['printf', '(', '"it is odd!\\n"', ')', ';'], ';'], ['return', 1, ';']], '}']], ['if', ['(', ['a', '%', 11], ')'], ['{', [[['printf', '(', '"divisible by 11\\n"', ')', ';'], ';'], ['return', 1, ';']], '}']]], ['return', 0, ';']], '}']]]
    '''
    def get_function_without_io(self, function_name, function):
        import re
        from regenerator import solve
        flattened_function = "".join([str(token) for token in solve(0,len(function),function)])
        mod_function = re.sub(r"printf\(.*?\);", "", flattened_function)
        if mod_function == flattened_function:
            self.change_pred = False
            return ''
        self.change_pred = True
        mod_function = re.sub(function_name, function_name + self.salt, mod_function)
        return mod_function

    def add_predicate(self,function):
        import re
        print("function: ", function)
        self.predicates[function[1]] = function

    def disp(self):
        for ds in self.tagged_data_structures:
            print(f"{ds}---->{self.tagged_data_structures[ds]}")

    ''' checks if sentinel search is possible '''
    def validate_linear_search(self,sub_tree):
        # print("In validate : ", sub_tree)
        for predicate in self.predicates:
            predicate_without_print = self.get_function_without_io(predicate, self.predicates[predicate])
            self.predicates[predicate].append([predicate_without_print])
        self.linear_to_sentinel(sub_tree)

    def find_loop_var(self,condition,name_ds):
        import re
        pat = f"{name_ds}" + r"\[(.*?)\]"
        # print("asdasdasdas ", name_ds, ''.join(flatten(condition)))

        match_object = re.search(pat, ''.join(([str(j) for j in flatten(condition)])))
        if(match_object):
            return match_object.groups(1)[0]
        print("no match for loop variable!!")

    def check_predicate(self,element):
        print("element : ", element)
        if(type(element[1]) == list and type(element[1][0]) != list and self.predicates[element[1][0]]):
            return True
        return False

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
            if(len(found_condition_raw) == 1 and self.check_predicate(found_condition_raw[0])):
                insert_code, name, hash = self.add_sentinel_predicate(found_condition_raw[0], found_condition_raw[0][1][0])
                print("\n\ninsert code predicate : ", insert_code)
                bounds_condition.insert(-1, '-')
                bounds_condition.insert(-1, '1')
                loop_var = self.find_loop_var(found_condition_raw[0], name)
                sub_condition = "".join(flatten(found_condition_raw[0]))
                sub_condition = re.sub(f"\[{loop_var}\]", f'[n{hash} - 1]', sub_condition)

                # substituting all predicate calls with calls to modified predicates

                if self.change_pred:
                    for predicate_name in self.predicates:
                        sub_condition = re.sub(predicate_name, predicate_name+self.salt, sub_condition)

                sub_body = ''.join(found_body_new[0])
                sub_tree.append(f"{name}[n{hash} - 1] = temp{hash};")

                sub_tree.append(['if(', bounds_condition, f'|| {sub_condition})', sub_body])
                sub_tree.insert(0, insert_code)
            else:
                insert_code, name, hash = self.add_sentinel(found_condition_raw[0])
                print("\n\ninsert code : ", insert_code)
                if(not insert_code):
                    return
                bounds_condition.insert(-1, '-')
                bounds_condition.insert(-1, '1')
                loop_var = self.find_loop_var(found_condition_raw[0], name)
                print("Loop_var: ", loop_var)
                sub_tree.append(f"{name}[n{hash} - 1] = temp{hash};")
                for idx in range(len(found_condition_raw)):
                    sub_condition = ''.join([str(j) for j in flatten(found_condition_raw[idx])])
                    sub_condition = re.sub(f"\[{loop_var}\]", f'[n{hash} - 1]', sub_condition)
                    sub_body = ''.join(found_body_new[idx])
                    sub_tree.append(['if(', bounds_condition, f'|| {sub_condition})', sub_body])
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

        def find(i, n, sub_tree, condition, body):
            if(i == n):
                return
            if(type(sub_tree[i]) == list and sub_tree[i][0] == 'if' and check_break(sub_tree[i][2])):
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
        return (condition_list, body_list)

    ''' adds sentinel value to end of tagged ds '''
    def add_sentinel(self, condition):
        import re
        flattened_condition = ''.join([str(j) for j in flatten(condition)])
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
        code = ""
        if(sentinel != ""):
            code = f"int n{hash} = sizeof({name}) / sizeof(int);"
            code += f"int temp{hash} = {name}[n{hash} - 1];"
            code += f" {name}[n{hash} - 1] = {sentinel};"
        return code, name, hash

    def add_sentinel_predicate(self,condition, fn_name):
        import re

        flattened_condition = ''.join([str(j) for j in flatten(condition)])
        flattened_condition = re.sub(r"\(", r" ( ", flattened_condition)
        flattened_condition = re.sub(r"\)", r" ) ", flattened_condition)
        pat = r"\s([^()]*?)\["
        m = re.search(pat, flattened_condition)
        name = ''
        if(m):
            name = m.group(1)

        sentinel = self.find_sentinel(fn_name)
        # print("name, sentinel : ", name, sentinel)
        hash = secrets.token_hex(nbytes=4)
        code = f"int n{hash} = sizeof({name}) / sizeof(int);"
        code += f"int temp{hash} = {name}[n{hash} - 1];"
        code += f" {name}[n{hash} - 1] = {sentinel};"
        return code, name, hash

    def check_canonical_form(self, predicate):
        """Check canonical form."""
        import re
        mod_predicate = re.sub("/\*.*?\*/", "", predicate)
        return_string = "return (.*?);"
        m = re.findall(return_string, mod_predicate)
        if(m and len(m) == 1):
            # print("asdasdsad ", m)
            return m[0]
        return None

    def find_sentinel(self, fn_name):
        """Find Sentinel."""
        from regenerator import solve
        import subprocess
        import re
        
        print("predicate name : ", self.predicates[fn_name][5][0][1][1])
        headers = "#include<stdio.h>\n#include<stdlib.h>\n"
        predicate = "".join(solve(0, len(self.predicates[fn_name]), self.predicates[fn_name]))
        expression = self.check_canonical_form(predicate)
        print("\n\nexpression\n\n", expression)
        bitwise_match = re.search("(?:[^&]+?(?:[&|^~])[^&]+?)|.+?(?:(?:<<)|(?:>>)).+?", expression)
        if(expression and not bitwise_match):
            sentinel = equation_solve(expression)
        else:
            main = '\nint main() {\nFILE *fptr;\nfptr = fopen("sentinel_res.txt","w");\nif(fptr == NULL){\nprintf("Error!");\nexit(1);\n}\nfor(int i = -100; i < 101; ++i){\n' + f'if({fn_name}(i))'+ '{\nfprintf(fptr, "%d", i);\nbreak;\n}\n}fclose(fptr);\n}'
            with open("find_sentinel.c", "w") as f:
                f.write(headers + predicate + main)
            subprocess.call(["gcc find_sentinel.c -o sentinel.out"], shell = True)
            subprocess.call(["./sentinel.out"], shell = True)
            with open("sentinel_res.txt", "r") as f:
                sentinel = int("".join(f.readlines()))

            subprocess.call(["rm find_sentinel.c sentinel_res.txt sentinel.out "], shell = True)

        return sentinel

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
