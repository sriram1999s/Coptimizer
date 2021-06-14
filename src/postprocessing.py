import re


def post_process(output_program):
    pat = ';+'
    output_program = re.sub(pat, ';', output_program)
    output_program = re.sub('(?:{;})+', '', output_program)
    output_program = re.sub('{;', '{', output_program)
    # print(re.search('{;}',output_program))
    check_prg = ''
    with open("check.c", "r") as f:
        check_prg = f.read()

    def nuke(m):
        return check_prg + m.group(0)

    output_program = re.sub('(int\s*main\(.*?\))', nuke, output_program)

    return output_program