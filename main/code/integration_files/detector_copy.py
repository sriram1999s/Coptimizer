import sys

from preprocessing import *
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
lines = pre_process(lines)
# log = logging.getLogger()
z=parser.parse(lines)

#print("AST:")
#print(z)
# print()
# print()
fn_defn_list.sort(key = lambda x:x[0])
fn_defn_obj_list.sort(key = lambda x:x.name)
#fn_call_list.sort(key = lambda x:x[0])
#fn_call_obj_list.sort(key = lambda x:x.name)
cyc_chk = []
non_in_fn = []
# print("\nz before : \n",z)

tail_rec_eli_solve(0,len(z),z);

fn_inline_solve(0,len(z),z,cyc_chk,non_in_fn);
#remove_unwanted_defns(0,len(z),z,non_in_fn)
# print("\nz after : \n",z)
output_prg=[]
solve(0,len(z),z,output_prg)
# print("\n\nnon_in_fn : ",non_in_fn,"\n\n")
# print("\n\nz :",z,"\n\n")
# print("\n\noutput_prg : \n",output_prg,"\n\n")

# with open("temp.c","w+") as f :
#     f.write("".join(output_prg))
# print("generated code")
print("".join(output_prg))

#----------------------------------IO handling -----------------------------------------------------------------------------
