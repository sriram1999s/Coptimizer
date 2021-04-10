import re

def post_process(output_program):
    pat = ';+'
    output_program = re.sub(pat,';',output_program)
    output_program = re.sub('(?:{;})+','',output_program)
    output_program = re.sub('{;','{',output_program)
    #print(re.search('{;}',output_program))
    return output_program
