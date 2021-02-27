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
with open("parse_track", 'w') as fp:
    fp.write('1')
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

# print('Func defn obj dict:')
# for i in fn_defn_obj_dict:
#     print(i, fn_defn_obj_dict[i].ret_type, fn_defn_obj_dict[i].fn_name, fn_defn_obj_dict[i].formal_parameters, fn_defn_obj_dict[i].inline_flag, fn_defn_obj_dict[i].return_id_or_val)
# print('Func call obj dict:')
# for i in fn_call_obj_dict:
#     for j in range(len(fn_call_obj_dict[i])):
#         print(i, fn_call_obj_dict[i][j].fn_name, fn_call_obj_dict[i][j].actual_arguments, fn_call_obj_dict[i][j].return_into)


with open("parse_track", 'w') as fp:
    fp.write('2')

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z=parser.parse(lines)

print("AST2:")
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


#----------------------------------IO handling -----------------------------------------------------------------------------