import sys
import re
sys.setrecursionlimit(10**9)
from parser import *

lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except :
    print('No arguments')

#------------------------------------IO handling --------------------------------------------------------------------------

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z=parser.parse(lines)

print("AST:")
print(z)
print()
print()
output_prg=[]
solve(0,len(z),z,output_prg)
#print(output_prg)
print("generated code")
print("".join(output_prg))

#----------------------------------IO handling -----------------------------------------------------------------------------
