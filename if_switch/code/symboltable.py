from collections import defaultdict
import re

level = '%'
level_str = []
symbol_table = defaultdict(lambda: 'garbage')


def make_level_string(var):
    global level_str
    global symbol_table
    copy_level_str = level_str.copy()
    search_string = str(var) + ''.join(copy_level_str)
    while (symbol_table[search_string] == 'garbage' and len(copy_level_str) > 1):
        copy_level_str.pop()
        search_string = str(var) + ''.join(copy_level_str)
    return search_string


def lookahead(i, n, l):
    global symbol_table
    global level_str
    if (i == n):
        return

    if (type(l[i]) == list):
        flag = True
        if (check_type(l[i]) == 0):
            flag = False
        if (flag):
            id = ''
            change = False
            if (len(l[i]) == 2):
                for k in l[i]:
                    if (type(k) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', k)):
                        id = k;
                        change = True
            else:
                ind_id = 0
                op_ind = 0
                f = False
                for k in l[i]:
                    if (type(k) == str and re.search('[A-Za-z_][A-Za-z_0-9]*', k)):
                        if (f == False):
                            id = k
                            change = True
                            break
                    if (type(k) == str and re.search('[^<>!=]?=', k)):
                        f = True
            if (change):
                search_str = id + '_'.join(level_str)
                pointer_search_str = '*' + search_str

                copy_level_str = level_str.copy()
                while (symbol_table[pointer_search_str] == 'garbage' and len(copy_level_str) > 1):
                    copy_level_str.pop()
                    pointer_search_str = id + '_'.join(copy_level_str)

                if (symbol_table[pointer_search_str] != 'garbage' and type(symbol_table[pointer_search_str]) == str):
                    rhs_search_str = symbol_table[pointer_search_str] + '_'.join(level_str)
                    copy_level_str = level_str.copy()
                    while (symbol_table[rhs_search_str] == 'garbage' and len(copy_level_str) > 1):
                        copy_level_str.pop()
                        rhs_search_str = id + '_'.join(copy_level_str)
                    if (symbol_table[rhs_search_str] != 'garbage'):
                        symbol_table[rhs_search_str] = 'declared'

                copy_level_str = level_str.copy()
                while (symbol_table[search_str] == 'garbage' and len(copy_level_str) > 1):
                    copy_level_str.pop()
                    search_str = id + '_'.join(copy_level_str)
                if (symbol_table[search_str] != 'garbage'):
                    symbol_table[search_str] = 'declared'
        else:
            lookahead(0, len(l[i]), l[i])

    lookahead(i + 1, len(l), l)


'''check whether type of variable is list (helper fxn)'''


def check_type(l):
    for i in l:
        if (type(i) == list):
            return 0
    return 1
