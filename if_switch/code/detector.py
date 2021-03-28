import sys
import re
import copy
import secrets
import uuid
import sys

sys.setrecursionlimit(10 ** 9)
from parser_file import *
from stack_match2 import *

lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except:
    print('No arguments')

# ------------------------------------IO handling --------------------------------------------------------------------------

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z = parser.parse(lines)

# print("AST:")
# print(z)
# print()
# print()

output_prg = []
solve(0, len(z), z, output_prg)
print("output_prg :\n", output_prg, "\n\n")

# with open("temp.c", "w+") as f:
#     f.write("".join(output_prg))
# print("".join(output_prg))

identify_chains(output_prg)
print('Dict num list of chains')
for i in dict_num_list_of_chains:
    print(i, ':')
    for j in dict_num_list_of_chains[i]:
        for k in j:
            print(k.type1, k.condition_vars, '->', end=' ')
        print()

from switch import *
make_switch(output_prg)
print('z2', z_new)
with open("temp.c", "w+") as f:
    f.write("".join(z_new))
print("".join(z_new))
# ----------------------------------IO handling -----------------------------------------------------------------------------