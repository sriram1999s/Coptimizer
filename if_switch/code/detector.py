import sys
import re
import copy
import secrets
import uuid
import sys

sys.setrecursionlimit(10 ** 9)
from parser_file import *
from function_inline import *

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

print("AST:")
print(z)
print()
print()

output_prg = []
solve(0, len(z), z, output_prg)
print("\n\noutput_prg : \n", output_prg, "\n\n")

with open("temp.c", "w+") as f:
    f.write("".join(output_prg))
print("".join(output_prg))

# ----------------------------------IO handling -----------------------------------------------------------------------------