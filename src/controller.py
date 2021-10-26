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
from optimizations.bit_hacks import validate_find_abs

''' init lexxer and parser '''
lexer = lex()
parser = yacc()

''' reading input '''
try:
    file = sys.argv[1]
except :
    print('No arguments')

dir_path = os.environ['COPTIMIZER_PATH']

''' reading optimizer flags '''
with open(f"{dir_path}/env/flags.json", "r") as inp:
    flags = json.load(inp)
    print("flags ", flags)
    menu.set(flags)
print("flags ", flags)
#------------------------------------IO handling --------------------------------------------------------------------------

''' reading input file '''
lines = ""
with open(file) as f:
    for line in f:
        lines += line
    # lines.strip('\n')
''' pre-processing '''
lines = pre_process(lines)

''' parsing '''
z=parser.parse(lines)


z = validate_find_abs(z)


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

''' cache algos '''
if(menu.FLAG_CACHE):
    cache.retain_outer_loop()
    cache.find_frequency_index()
    for key in cache.for_loops:
        print(f"{key}---->{''.join(solve(0, len(cache.for_loops[key]), cache.for_loops[key]))}")


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

''' writing output to temporary file '''
with open("temp.c","w+") as f :
    f.write(output_prg)
# print("z_new", z_new)

''' printing to stdout '''
print("generated code")
print(output_prg)

#----------------------------------IO handling -----------------------------------------------------------------------------
