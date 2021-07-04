import re
import os

'''preprocessing handler'''
def pre_process(text):
    '''regex to detect <=/>= to </> for operator consistency'''
    pat1 = '(for\s*\(.*?)(<|>)=\s*(.*?)([\s;)])'
    text = re.sub(pat1 ,remove_rel_assign ,text)

    '''regex to detect single line commaents and convert to multiline comments'''
    pat3 = r'//(.*?)\n'
    text = re.sub(pat3, change_to_multiline, text)
    
    '''regex to detect newline and remove it'''
    pat4 = r'\n'
    text = re.sub(pat4, '', text)
   
    print("Printing preprocessed text...\n")
    print(text,"\n\n")

    '''flag generation for input detection in the C code'''
    dir_path = os.environ['COPTIMIZER_PATH']
    with open(f'{dir_path}/env/check_input', 'w') as file:
        check_inp = '(?:scanf\()|(?:gets\()|(?:getc\()'
        if(re.search(check_inp, text)):
            file.write('1')
        else:
            file.write('0')
    return text

'''replaces relational operators(called when pat1 matched)'''
def remove_rel_assign(m):
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

'''callback to replace single line comments to multiline comments(pat3)'''
def change_to_multiline(m):
    return '/*' + m.group(1) + '*/'
