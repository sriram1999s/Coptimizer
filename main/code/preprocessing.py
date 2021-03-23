import re
def pre_process(text):
    pat1 = '(<|>)=\s*(.*?)([;)])'
    text = re.sub(pat1 ,remove_rel_assign ,text)
    pat2 = 'void.*?{(.*?)}'
    re.sub(pat2 ,return_void ,text)
    print("Printing preprocessed text...\n")
    print(text,"\n\n")
    return text

def remove_rel_assign(m):
    # print(m.groups(0))
    if(m.group(1)=='<'):
        new_val = str(int(m.group(2))+1)
    if(m.group(1)=='>'):
        new_val = str(int(m.group(2))-1)
    return m.group(1) + new_val + m.group(3)

def return_void(m):
    print("here")
    print(m.groups(0))
