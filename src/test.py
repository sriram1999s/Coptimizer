from sympy import reduce_inequalities
from sympy.abc import x
from collections.abc import Iterable
from lexer import *
from parser import *
import re
import sys

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
    # print(x1, y1, x2, y2)
    if(x2 <= x1 <= y2 or x2 <= y1 <= y2):
        return 1
    elif(min(x1, y1) > min(x2, y2) and max(x1, y1) < max(x2, y2)):
        return 1

    elif(min(x1, y1) < min(x2, y2) and max(x1, y1) > max(x2, y2)):
        return 1
    return 0

    
def union(range1,range2):
    res_range = []
    if(check_not_nested(range1)):
        range1 = [range1]
    if(check_not_nested(range2)):
        range2 = [range2]
    print(f"ranges---->\n{range1}\n{range2}")
    for range_i in range1:
        for range_j in range2:
            x1, y1, x2, y2 = range_i[0], range_i[1], range_j[0], range_j[1]
            if(check_overlap(x1, y1, x2, y2)):
                res_range += [[min(x1, x2), max(y1, y2)]]
                # print("res range: ", res_range)
            else:
                # [] + [[x1,y1],[x2,y2]]
                res_range += [range_i, range_j]
    return res_range

def intersection(range1, range2):
    res_range = []
    if(check_not_nested(range1)):
        range1 = [range1]
    if(check_not_nested(range2)):
        range2 = [range2]
    print(f"ranges---->\n{range1}\n{range2}")
    for range_i in range1:
        for range_j in range2:
            x1, y1, x2, y2 = range_i[0], range_i[1], range_j[0], range_j[1]
            if(check_overlap(x1, y1, x2, y2)):
                res_range += [[max(x1, x2), min(y1, y2)]]
    return res_range

def check_not_nested(l):
    for i in l:
        if(type(i) == list):
            return False
    return True

def max_one_level_nest(l):

    flattened = list(flatten(l))
    print("flattened", flattened)
    if(flattened.count('||') > 0 or flattened.count('&&') > 0):
        print("logical op found ")
        return False

    for i in l:
        if(type(i) == list):
            for j in i:
                if(type(j) == list):
                    return False
    return True

def find_ultimate(i,n,l):
    """Finds the solution space."""
    if(i == n):
        return []

    # print("l", l)
    #[1,2]
    if(type(l) == list and len(l) == 2 and check_not_nested(l)):
        print("base case 1: ", l)
        return l

    #[[[a1, b1], [a2, b2]],'||',[[c1, d1], [c2, d2]]
    if(type(l) == list and len(l) == 3 and max_one_level_nest(l[0]) and max_one_level_nest(l[2])):
        print("base case 2.1: ", l)
        if(l[1] == "&&"):
            return intersection(l[0], l[2])
        elif(l[1] == "||"):
            return union(l[0], l[2])
    
    #[1,2]
    if(type(l[i]) == list and len(l[i]) == 2 and check_not_nested(l[i])):
        print("base case 1: ", l[i])
        return l[i]

    #[[[a1, b1], [a2, b2]],'||',[[c1, d1], [c2, d2]]
    if(type(l[i]) == list and len(l[i]) == 3 and max_one_level_nest(l[i][0]) and max_one_level_nest(l[i][2])):
        print("base case 2: ", l[i])
        if(l[i][1] == "&&"):
            l[i] = intersection(l[i][0], l[i][2])
        elif(l[i][1] == "||"):
            # print("union: ",l[i])
            l[i] = union(l[i][0], l[i][2])
        return l[i]

    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][1])==str):
        print("before", l[i])
        left = find_ultimate(0, len(l[i][0]), l[i][0])
        right = find_ultimate(0, len(l[i][2]), l[i][2])
        l[i][0], l[i][2] = left, right
        print("intermediate ", l[i])
        if(l[i][1] == "&&"):
            l[i] = intersection(l[i][0], l[i][2])
        elif(l[i][1] == "||"):
            # print("union: ",l[i])
            l[i] = union(l[i][0], l[i][2])
        print("after", l[i])
        
    return find_ultimate(i+1, n, l)

lexer = lex()
parser = yacc()




    
expr1 = "(2*x>9) || ((x<7) && (x>1));"
expr2 = "(((x<-3) || (x>3)) && (x>4)) || (x<-2);"
l = parser.parse(expr2)

print("l before", l)
convert_inequality_to_interval(0, len(l), l)
print("l after", l)
print("\n\n\n")
res = find_ultimate(0, len(l), l)
print(l)
