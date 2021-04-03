import re

def post_process(output_program):
    pat = r';+'
    output_program = re.sub(pat,';',output_program)
    return output_program