from sympy import reduce_inequalities
from sympy.abc import x
from collections.abc import Iterable
from lexer import *
from parser import *
import re
import sys

# expr = "2*x < 7"

# parsed_range = reduce_inequalities(expr,[])
# print(str(parsed_range))

def flatten(l):
    """Eliminates the nested nature of an iterable for convenient processing."""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def eval(fraction):
    parts = fraction.split('/')
    if(len(parts) > 1):
        return int(parts[0])//int(parts[1])
    return int(fraction)

def construct_interval(parsed_range):

    right_capture = r"\(.*?x.*?<(.*?)\)"
    left_capture = r"\((.*?)<.*?x.*?\)"

    interval = []
    left_match = re.search(left_capture, parsed_range)
    right_match = re.search(right_capture, parsed_range)
    if(left_match):
        capture = left_match.group(1).strip(" ")
        if(capture == '-oo'):
            capture = -sys.maxsize
        elif(capture == 'oo'):
            capture = sys.maxsize
        if(type(capture) == str):
            interval.append(eval(capture))
        else:
            interval.append(capture)

    if(right_match):
        capture = right_match.group(1).strip(" ")
        if(capture == '-oo'):
            capture = -sys.maxsize
        elif(capture == 'oo'):
            capture = sys.maxsize
        if(type(capture) == str):
            interval.append(eval(capture))
        else:
            interval.append(capture)
    return interval

def convert_inequality_to_interval(i,n,l):
    """Recursive function to convert."""
    if(i == n):
        return
    
    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][1])==list and (l[i][1][1] == '<' or l[i][1][1] == '>')):
        temp = [str(tok) for tok in flatten(l[i])]
        solution = reduce_inequalities("".join(temp), [])
        l[i] = construct_interval(str(solution))
        
    if(type(l[i]) == list):
        l[i] = [tok for tok in l[i] if tok not in ['(', ')']]
        if(len(l[i]) == 1 and type(l[i][0]) == list):
            l[i] = l[i][0]
        convert_inequality_to_interval(0, len(l[i]), l[i])
    convert_inequality_to_interval(i+1, n, l)


def check_overlap(x1, y1, x2, y2):
    print(x1,y1,x2,y2)
    if(x2<=x1<=y2 or x2<=y1<=y2):
        return 1
                    # [1,3] , [0,4]
    elif(min(x1,y1) > min(x2,y2) and max(x1,y1) < max(x2,y2)):
        return 1

    elif(min(x1,y1) < min(x2,y2) and max(x1,y1) > max(x2,y2)):
        return 1
    return 0

    
def union(range1,range2):
    x1,y1,x2,y2 = range1[0],range1[1],range2[0],range2[1]
    res_range = []
    if(check_overlap(x1, y1, x2, y2)):
        res_range += [min(x1,x2),max(y1,y2)]
        print("res range: ", res_range)
    else:
        res_range += [range1, range2]
    return res_range

def intersection(range1, range2):
    x1,y1,x2,y2 = range1[0],range1[1],range2[0],range2[1]
    res_range = []
    if(check_overlap(x1, y1, x2, y2)):
        res_range += [max(x1,x2),min(y1,y2)]
        print("res_range: ",res_range,range1,range2)
        return res_range
    return None

def check_not_nested(l):
    for i in l:
        if(type(i) == list):
            return False
    return True

def find_ultimate(i,n,l):
    """Finds the solution space."""
    if(i == n):
        return []

    #print("l", l)
    if(type(l) == list and len(l) == 2 and check_not_nested(l)):
        print("base case 1: ", l)
        return l

    if(type(l) == list and len(l) == 3 and len(l[0]) == 2 and len(l[2]) == 2):
        print("base case 2: ", l)
        if(l[1] == "&&"):
            return intersection(l[0], l[2])
        elif(l[1] == "||"):
            return union(l[0], l[2])
    
    
    if(type(l[i]) == list and len(l[i]) == 2 and check_not_nested(l[i])):
        print("base case 1: ",l[i])
        return l[i]
    
    if(type(l[i]) == list and len(l[i]) == 3 and len(l[i][0]) == 2 and len(l[i][2]) == 2):
        print("base case 2: ", l[i])
        if(l[i][1] == "&&"):
            return intersection(l[i][0], l[i][2])
        elif(l[i][1] == "||"):
            # print("union: ",l[i])
            return union(l[i][0], l[i][2])

    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][1])==str):
        #print("before", l[i])
        left = find_ultimate(0, len(l[i][0]), l[i][0])
        right = find_ultimate(0, len(l[i][2]), l[i][2])
        l[i][0],l[i][2] = left,right
        if(l[i][1] == "&&"):
            l[i] = intersection(l[i][0], l[i][2])
        elif(l[i][1] == "||"):
            # print("union: ",l[i])
            l[i] = union(l[i][0], l[i][2])
        #print("after", l[i])
        
    return find_ultimate(i+1, n, l)

''' init lexxer and parser '''
lexer = lex()
parser = yacc()




    
expr = "(2*x>9) || ((x<7) && (x>1));"
l = parser.parse(expr)

print("l before", l)
convert_inequality_to_interval(0, len(l), l)
print("l after", l)
print("\n\n\n")
res = find_ultimate(0, len(l), l)
print(res,l)
