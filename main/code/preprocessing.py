import re
def pre_process(text):
    pat1 = '(<|>)=\s*(.*?)([;)])'
    text = re.sub(pat1 ,remove_rel_assign ,text)
    pat2 = '(for\(.*?\))([^{].*?;)'
    text = re.sub(pat2 ,add_brace ,text)
    # print(text)
    return text

def remove_rel_assign(m):
    # print(m.groups(0))
    if(m.group(1)=='<'):
        new_val = str(int(m.group(2))+1)
    if(m.group(1)=='>'):
        new_val = str(int(m.group(2))-1)
    return m.group(1) + new_val + m.group(3)

def add_brace(m):
    # print(m.groups(0))
    return m.group(1) + '{' + m.group(2) + '}'
