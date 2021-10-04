from sympy import reduce_inequalities
from sympy.abc import x
from collections.abc import Iterable
from lexer import *
from parser import *
import re

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


def construct_interval(parsed_range):

    right_capture = r"\(.*?x.*?<(.*?)\)"
    left_capture = r"\((.*?)<.*?x.*?\)"

    interval = []
    left_match = re.search(left_capture, parsed_range)
    right_match = re.search(right_capture, parsed_range)
    if(left_match):
        interval.append(left_match.group(1).strip(" "))
    if(right_match):
        interval.append(right_match.group(1).strip(" "))
    return interval

def convert_inequality_to_interval(i,n,l):
    """Recursive function to sonvert."""
    if(i == n):
        return
    
    if(type(l[i]) == list and len(l[i]) == 3 and type(l[i][1])==list and (l[i][1][1] == '<' or l[i][1][1] == '>')):
        temp = [str(tok) for tok in flatten(l[i])]
        solution = reduce_inequalities("".join(temp), [])
        l[i] = construct_interval(str(solution))
        
    if(type(l[i]) == list):
        convert_inequality_to_interval(0, len(l[i]), l[i])
    convert_inequality_to_interval(i+1, n, l)

''' init lexxer and parser '''
lexer = lex()
parser = yacc()




    
expr = "(2*x>9) || ((x<7) && (x>1));"
l = parser.parse(expr)

print("l before", l)
convert_inequality_to_interval(0, len(l), l)
print("l after", l)
