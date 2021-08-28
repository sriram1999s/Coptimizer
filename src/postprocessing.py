import re
import os

def post_process(output_program):

    ''' removes redundant semicolons '''
    pat = ';+'
    output_program = re.sub(pat,';',output_program)
    ''' removes redundant semicolons '''
    output_program = re.sub('(?:{;})+','',output_program)
    ''' removes redundant semicolons '''
    output_program = re.sub('{;','{',output_program)

    check_prg = ''
    dir_path = os.environ['COPTIMIZER_PATH']

    ''' overlap handler for compile time initialization '''
    with open(f"{dir_path}/env/check.c","r") as f:
        check_prg = f.read()


    ''' does the substitution for overlap handling '''
    def nuke(m):
        return check_prg + m.group(0)
    output_program = re.sub('(int\s*main\(.*?\))',nuke,output_program)


    return output_program
