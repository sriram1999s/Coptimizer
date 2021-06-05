import secrets
def gen_check():
    fn_hash = secrets.token_hex(nbytes=6)
    fn_dec = 'int' + ' check_overlap' + fn_hash + '(int x1, int y1, int x2, int y2) {'

    return_1 = 'return 1;'
    return_0 = 'return 0;'

    first_condition = 'if((x1>=x2 && x1<y2) || (y1>x2 && y1<=y2) || '
    second_condition = '((x1<y1?x1:y1) > (x2<y2?x2:y2) && (x1>y1?x1:y1) < (x2>y2?x2:y2)) ||'
    third_condition = '((x1<y1?x1:y1) < (x2<y2?x2:y2) && (x1>y1?x1:y1) > (x2>y2?x2:y2)))'

    final_condition = fn_dec + first_condition + second_condition + third_condition + return_1 + return_0 + '}';
    return final_condition

print(gen_check())
