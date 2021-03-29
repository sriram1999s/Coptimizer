import sys
from preprocessing import *
from postprocessing import *
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
print()
print()
output_prg=[]
solve(0,len(z),z,output_prg)
# print(output_prg)

output_prg = "".join(output_prg)
output_prg = make_compile_inits(output_prg)

output_prg = post_process(output_prg)

with open("temp.c","w+") as f :
    f.write(output_prg)
print("generated code")
print(output_prg)

#----------------------------------IO handling -----------------------------------------------------------------------------
