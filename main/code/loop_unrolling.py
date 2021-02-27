from regenerator import *

def for_unroll_validate(sub_tree):
    condition = sub_tree[1]
    output = []
    print("Printing condition : ", condition)
    # print(sub_tree)
    res = []

    if(condition[1][0] == 'int' or condition[1][0] == 'float'): # checking for declaration
        if(type(condition[1][3]) == str or type(condition[1][3]) == list ): # LHS is variable / expression
            # print("Here1-----")
            return sub_tree
    else:
        if(type(condition[1][2]) == str or type(condition[1][2]) == list ): # LHS is variable / expression
            # print("Here2-----")
            return sub_tree

    if(type(condition[2]) == list): # checking for declaration
        ind = 2
    else:
        ind = 3

    if(type(condition[ind][0]) == list or type(condition[ind][2]) == list): # LHS or RHS of bounds check is not an expression
        # print("here")
        return sub_tree

    if(type(condition[ind][2])==int ): # LHS of bounds check is an integer
        if(condition[ind][2] <= 35): # full unrolling
            solve(0,len(sub_tree[2]),sub_tree[2],output) #remove nesting in sub_tree[2]
            unrolled = for_full_unroll(output, condition)
            res = [unrolled]
        else:
            solve(0,len(sub_tree[2]),sub_tree[2],output)
            unrolled = for_partial_unroll(output, condition)
            res = [sub_tree[0],sub_tree[1],unrolled]
    return res

def for_full_unroll(block, condition):
    block.pop(0)
    block.pop()
    res=[]
    find_int(0,len(condition),condition,res) # to get start and end value of loop by scanning for integer
    #print(res)
    return block * (abs(res[0][0]-res[1][0]))

def for_partial_unroll(block, condition):
    block.pop(0)
    block.pop()
    res=[]
    find_int(0,len(condition),condition,res)
    total = abs(res[0][0]-res[1][0])
    factor = 0.5
    unroll_count = int(total*factor)
    #print(total,unroll_count)
    #print(res)
    #print(condition[2][res[1][-1]])
    condition[2][res[1][-1]] = total//unroll_count + res[0][0] #readjusting the end value of loop after partial unrolling
    # = res[1]//unroll_count
    extra = total%unroll_count
    return ['{']+block*unroll_count+['}'] + block*extra


def find_int(i,n,l,res=[]):
    #print(l,i,level)
    if(i==n):
        return
    if(type(l[i]) is int):
        res.append([l[i],i])
    elif(type(l[i]) is list):
        find_int(0,len(l[i]),l[i],res)
    find_int(i+1,n,l,res)
