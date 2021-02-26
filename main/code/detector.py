import sys
import re
sys.setrecursionlimit(10**9)
from parser_file import *
from function_inline import *

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
with open("temp.c","w+") as f :
    f.write("".join(output_prg))
print("generated code")
print("".join(output_prg))

print('Func defn list:')
for i in range(len(fn_defn_list)):
    print(i, fn_defn_list[i])

print('\nFunc call list:')
for i in range(len(fn_call_list)):
    print(i, fn_call_list[i])
#----------------------------------IO handling -----------------------------------------------------------------------------
