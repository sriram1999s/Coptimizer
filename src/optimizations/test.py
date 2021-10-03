from sympy import *
from sympy.abc import x
import re

expr = 2*x < 7

parsed_range = reduce_inequalities(expr,[])
print(str(parsed_range))

def construct_interval(parsed_range):
    right_capture = "\(.*?x.*?<(.*?)\)"
    left_capture =  "\((.*?)<.*?x.*?\)"

    interval = []
    left_match = re.search(left_capture, parsed_range)
    right_match = re.search(right_capture, parsed_range)
    if(left_match):
        interval.append(left_match.group(1).strip(" "))
    if(right_match):
        interval.append(right_match.group(1).strip(" "))
    return interval

print(construct_interval(str(parsed_range)))
        
        
