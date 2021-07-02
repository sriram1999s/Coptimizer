import sys
import json
from preprocessing import *
from postprocessing import *
sys.setrecursionlimit(10**9)
from parser import *
# from stack_match2 import *
# from switch import *

from optimizations.stack_match2 import *
from optimizations.switch import *

lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except :
    print('No arguments')

with open("flags.json", "r") as inp:
    flags = json.load(inp)
    menu.set(flags)
print("flags ", flags)
#------------------------------------IO handling --------------------------------------------------------------------------


lines = ""
with open(file) as f:
    for line in f:
        lines += line
    # lines.strip('\n')
''' pre processing '''
lines = pre_process(lines)
z=parser.parse(lines)


fn_defn_list.sort(key = lambda x:x[0])
fn_defn_obj_list.sort(key = lambda x:x.name)
cyc_chk = []
non_in_fn = []

''' tail end recursion '''
if(menu.FLAG_TAIL_RECURSION):
    tail_rec_eli_solve(menu.FLAG_INLINE, 0,len(z),z)

''' function inlining '''
if(menu.FLAG_INLINE):
    fn_inline_solve(0,len(z),z,cyc_chk,non_in_fn)

print("AST:")
print(z)
print()
print()
output_prg = solve(0,len(z),z)
# output_prg = solve_multithread(0,len(z),z)
''' if to switch '''
identify_chains(menu.FLAG_IF_TO_SWITCH, output_prg)
make_switch(menu.FLAG_IF_TO_SWITCH, output_prg)

if(menu.FLAG_IF_TO_SWITCH):
    output_prg = "".join(z_new)
else:
    output_prg = "".join(output_prg)

''' compile time inits '''
output_prg = com_init.make_compile_inits(menu.FLAG_COMPILE_INIT,output_prg)

''' post processing '''
output_prg = post_process(output_prg)


with open("temp.c","w+") as f :
    f.write(output_prg)
# print("z_new", z_new)

print("generated code")
print(output_prg)

#----------------------------------IO handling -----------------------------------------------------------------------------
