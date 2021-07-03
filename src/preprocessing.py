import re
import os

def pre_process(text):
    pat1 = '(for\s*\(.*?)(<|>)=\s*(.*?)([\s;)])'
    text = re.sub(pat1 ,remove_rel_assign ,text)
    # pat2 = 'void.*?{(.*?)}'
    pat3 = r'//(.*?)\n'
    text = re.sub(pat3, change_to_multiline, text)
    pat4 = r'\n'
    text = re.sub(pat4, '', text)
    # re.sub(pat2 ,return_void ,text)
    print("Printing preprocessed text...\n")
    print(text,"\n\n")

    dir_path = os.environ['COPTIMIZER_PATH']
    with open(f'{dir_path}/env/check_input', 'w') as file:
        check_inp = '(?:scanf\()|(?:gets\()|(?:getc\()'
        if(re.search(check_inp, text)):
            file.write('1')
        else:
            file.write('0')
    return text

def remove_rel_assign(m):
    # print(m.groups(0))
    if(m.group(2)=='<'):
        # print("in pre_process")
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

def change_to_multiline(m):
    # print(m.group(1))
    return '/*' + m.group(1) + '*/'
# def return_void(m):
    # print("here")
    # print(m.groups(0))
