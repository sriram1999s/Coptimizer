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


def remove_extra_brackets(z):
    i = 0
    seen_a = None
    z_inp = []
    extra = []
    net_open = 0

    while i<len(z):
        if z[i] == 'if':
            # if seen_a is not None:
            #     pop_extra(extra, z_inp)

            seen_a = 'if'
            z_inp.append(z[i])
            i+=1

        elif z[i] == 'else':
            if i+4<len(z) and z[i+1] == ' ' and z[i+2] == '{' and z[i+3] == ' ' and z[i+4] == 'if':
                seen_a = 'elif'
                z_inp.append(z[i])
                z_inp.append(z[i+1])
                z_inp.append(z[i+2])
                z_inp.append(z[i+3])
                z_inp.append(z[i+4])

                net_open +=1

                i+=5
            else:
                seen_a = 'else'
                z_inp.append(z[i])
                i+=1

        elif z[i] == '{':
            if seen_a is not None:

                net_open_before = net_open

                # e, i = count_extra(i, z)
                # extra.append(e)

                e, i, net_open = count_extra(i, z, net_open)
                extra.append((net_open_before, e))

                z_inp.append('{')
                seen_a = None
            else:
                z_inp.append(z[i])
                i+=1

                net_open +=1

        elif z[i] == '}':
            net_open -=1
            if extra and net_open == extra[-1][0]:
                pop_extra(extra, z_inp)
            z_inp.append(z[i])
            i += 1

        else:
            z_inp.append(z[i])
            i+=1

    if seen_a is not None:
        pop_extra(extra, z_inp)
    return z_inp


# def count_extra(pos, z):
def count_extra(pos, z, net_open):
    count = 0
    while pos<len(z) and z[pos]=='{':
        pos+=1
        count+=1

        net_open +=1

    return count-1, pos, net_open


def pop_extra(extra, z_inp):
    # e = extra[-1]

    e = extra[-1][1]

    while e>0:
        z_inp.pop()
        e-=1
    extra.pop()