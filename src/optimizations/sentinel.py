
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

    def validate_linear_search(self,sub_tree):
        print(sub_tree)
        

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
