import re
def pre_process(text):
    pat1 = '(for\(.*?)(<|>)=\s*(.*?)([\s;)])'
    text = re.sub(pat1 ,remove_rel_assign ,text)
    pat2 = 'void.*?{(.*?)}'
    # re.sub(pat2 ,return_void ,text)
    print("Printing preprocessed text...\n")
    print(text,"\n\n")
    return text

def remove_rel_assign(m):
    print(m.groups(0))
    if(m.group(2)=='<'):
        if(re.search('[a-zA-z_]+',m.group(3))):
            new_val = m.group(3)+'+1'
        else:
            new_val = str(int(m.group(3))+1)
    if(m.group(2)=='>'):
        if(re.search('\w+',m.group(3))):
            new_val = m.group(3)+'+1'
        else:
            new_val = str(int(m.group(3))+1)   
    return m.group(1) + m.group(2)  + new_val  + m.group(4)

# def return_void(m):
    # print("here")
    # print(m.groups(0))
