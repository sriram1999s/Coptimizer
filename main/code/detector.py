import sys
from preprocessing import *
from postprocessing import *
sys.setrecursionlimit(10**9)
from parser import *
from switch import *

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
''' pre processing '''
lines = pre_process(lines)
z=parser.parse(lines)


fn_defn_list.sort(key = lambda x:x[0])
fn_defn_obj_list.sort(key = lambda x:x.name)
cyc_chk = []
non_in_fn = []

''' tail end recursion '''
tail_rec_eli_solve(0,len(z),z);

''' function inlining '''
fn_inline_solve(0,len(z),z,cyc_chk,non_in_fn);

#print("AST:")
#print(z)
print()
print()
output_prg=[]
solve(0,len(z),z,output_prg)
# ''' if to switch '''
# make_switch(output_prg)

output_prg = "".join(output_prg)

''' compile time inits '''
output_prg = com_init.make_compile_inits(output_prg)

''' post processing '''
output_prg = post_process(output_prg)


with open("temp.c","w+") as f :
    f.write("".join(z_new))
# print("z_new", z_new)

print("generated code")
print(output_prg)

#----------------------------------IO handling -----------------------------------------------------------------------------
