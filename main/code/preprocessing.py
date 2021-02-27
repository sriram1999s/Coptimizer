import re
def remove_rel_assign(text):
    pat = '(<|>)=\s*(.*?)([;)])'
    text = re.sub(pat,change ,text)
    print(text)
    return text

def change(m):
    print(m.groups(0))
    if(m.group(1)=='<'):
        new_val = str(int(m.group(2))+1)
    if(m.group(1)=='>'):
        new_val = str(int(m.group(2))-1)
    return m.group(1) + new_val + m.group(3)
