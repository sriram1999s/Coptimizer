from ply.lex import lex
from ply.yacc import yacc
import sys
import re
import pprint

sys.setrecursionlimit(10 ** 9)

'''
READ THIS BEFORE ADDING CALLABLES
def fxn_name(t):
    'Docstring regex'
    any conditions if it might clash
    return t
t object has parameters:
1)value
2)type(as described in the tokens)
t -----> lexer object
p -----> production object
P.S: Try to stick to a single convention
'''

''' defining tokens '''

numbers = ['INT_NUM', 'FLOAT_NUM']

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'L_SHIFT', 'R_SHIFT', 'AND', 'OR', 'MOD', 'PLUS_PLUS', 'MINUS_MINUS']

logic = ['BIT_OR', 'BIT_AND', 'BIT_XOR']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

assignment = ['ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN',
              'XOR_ASSIGN', 'MOD_ASSIGN', 'L_SHIFT_ASSIGN', 'R_SHIFT_ASSIGN']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWBRACE', 'R_FLOWBRACE', 'SEMICOLON', 'COMMA']

statements = ['FOR', 'WHILE', 'IF', 'ELSE']

unary = ['NOT']

extra = ['ID', 'TYPE']

tokens = numbers + bin_op + logic + rel_op + assignment + delimiters + statements + unary + extra

# --------------------------------lexer------------------------------------ #

''' regular expressions defined here '''

# relational operators

t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_EQ = r'=='

# assignment (had to be after relop)

t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_MOD_ASSIGN = r'%='
t_L_SHIFT_ASSIGN = r'<<='
t_R_SHIFT_ASSIGN = r'>>='
t_ASSIGN = r'='

# delimiters

t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_FLOWBRACE = r'\{'
t_R_FLOWBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','

# unary

t_NOT = r'!'

# binary operators

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_L_SHIFT = r'<<'
t_R_SHIFT = r'>>'
t_AND = r'&&'
t_OR = r'\|\|'
t_MOD = r'%'
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'\-\-'

# logical operators

t_BIT_AND = r'\&'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'

# ignore

t_ignore = ' \t'


# while
def t_WHILE(t):
    r'while'
    return t


# if
def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


# for

def t_FOR(t):
    r'for'
    return t


# float

def t_FLOAT_NUM(t):
    r'\d+\.\d+'
    return t


# int

def t_INT_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


# types

def t_TYPE(t):
    r'int|float'
    return t


# identifiers

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


# error

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


# --------------------------------parser------------------------------------ #

# defining precedence of operators
# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULTIPLY', 'DIVIDE')
# )

# start = 'start'
def p_start(p):
    '''
    start : multiple_statements
    '''
    # print(p[1])
    p[0] = p[1]


def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''
    if (len(p) == 3):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]


def p_statement(p):
    '''
    statement : open
              | closed
    '''
    p[0] = p[1]


def p_open(p):
    '''
    open : IF condition statement
         | IF condition closed ELSE open
         | WHILE condition open
         | FOR for_condition open
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]


def p_closed(p):
    '''
    closed : simple
           | block
           | IF condition closed ELSE closed
           | WHILE condition closed
           | FOR for_condition closed
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        if (p[1] == 'for'):
            print("for detected")
            # p[0] = [p[1],p[2],p[3]]
            p[0] = for_unroll_validate([p[1], p[2], p[3]])
        else:
            print("while detected")
            # p[0] = [p[1], p[2], p[3]]
            p[0] = while_unroll_validate([p[1], p[2], p[3]])
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]


def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    p[0] = [p[1], p[2], p[3]]


def p_for_condition(p):
    '''
    for_condition : L_PAREN declaration expr SEMICOLON expr R_PAREN
    '''
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


def p_multi_declaration(p):
    '''
    multi_declaration : multi_declaration ID COMMA
                  | multi_declaration ID ASSIGN expr COMMA
              | ID COMMA
                  | ID ASSIGN expr COMMA
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        p[0] = p[1] + [p[2], p[3]]
    elif (len(p) == 6):
        p[0] = p[1] + [p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4]]


def p_stop(p):
    '''
     stop : ID SEMICOLON
      | ID ASSIGN expr SEMICOLON
     '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3], p[4]]


def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
        | TYPE multi_declaration stop
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]


def p_block(p):
    '''
    block : L_FLOWBRACE multiple_statements R_FLOWBRACE
    '''
    p[0] = [p[1], p[2], p[3]]


def p_simple(p):
    '''
    simple : expr SEMICOLON
           | declaration
           | SEMICOLON
       | function
       | function_call
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


def p_yes_dec_params(p):
    '''
    yes_dec_params : yes_dec_params TYPE ID COMMA
                    | TYPE ID COMMA
                    | empty
    '''
    if (len(p) == 5):
        p[0] = p[1] + [p[2], p[3], p[4]]
    elif (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = []


def p_end_dec_params(p):
    '''
    end_dec_params : TYPE ID
    '''
    p[0] = [p[1], p[2]]


def p_dec_params(p):
    '''
	dec_params : empty
	            | yes_dec_params end_dec_params
	'''
    if (len(p) == 3):
        p[0] = [p[1] + p[2]]
    else:
        p[0] = []


def p_call_params(p):
    '''
    	call_params : empty
		    | yes_call_params end_call_params
    '''
    if(len(p) == 3):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_yes_call_params(p):
    '''
    yes_call_params : yes_call_params INT_NUM COMMA
    		    | yes_call_params ID COMMA
		    | INT_NUM COMMA
		    | ID COMMA
	       	    | empty
    '''
    if(len(p)==0):
        p[0] = []
    elif(len(p)==3):
        p[0] = [p[1],p[2]]
    else:
        p[0] = p[1] + [p[2],p[3]]

def p_end_call_params(p):
    '''
    end_call_params : INT_NUM
		    | ID
    '''
    p[0] = p[1]
        
def p_function(p):
    '''
    function : TYPE ID L_PAREN dec_params R_PAREN function_2
    		  | ID L_PAREN call_params R_PAREN SEMICOLON
    '''
    if (len(p) == 7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]


def p_function_2(p):
    '''
    function_2 : SEMICOLON
               | block
    '''
    p[0] = [p[1]]


def p_function_call(p):
    '''
    function_call : ID L_PAREN call_params R_PAREN SEMICOLON
                    | TYPE ID ASSIGN ID L_PAREN call_params R_PAREN SEMICOLON
                    | ID ASSIGN ID L_PAREN call_params R_PAREN SEMICOLON
    '''
    if (len(p) == 6):
        p[0] = [p[1], p[2], p[3], p[4], p[5]]
    elif (len(p) == 9):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]


# def p_parameters(p):
#     '''
#     parameters : parameters TYPE ID COMMA stop
#          | stop
#     '''
#     if(len(p)==2):
#         p[0]=(p[1])
#     else:
#         p[0] = ((p[1]),p[2],p[3],p[4],p[5])

# def p_stop(p):
#     '''
#     stop : TYPE ID
#     '''
#     p[0] = (p[1],p[2])

def p_expr(p):
    '''
    expr : expr assignment exprOR
         | exprOR
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_assignment(p):
    '''
    assignment : ASSIGN
               | PLUS_ASSIGN
               | MINUS_ASSIGN
               | MUL_ASSIGN
               | DIV_ASSIGN
               | AND_ASSIGN
               | OR_ASSIGN
               | XOR_ASSIGN
               | MOD_ASSIGN
               | L_SHIFT_ASSIGN
               | R_SHIFT_ASSIGN
    '''
    p[0] = p[1]


def p_exprOR(p):
    '''
    exprOR : exprOR OR exprAND
           | exprAND
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprAND(p):
    '''
    exprAND : exprAND AND exprBITOR
            | exprBITOR
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITOR(p):
    '''
    exprBITOR : exprBITOR BIT_OR exprBITXOR
              | exprBITXOR
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITXOR(p):
    '''
    exprBITXOR : exprBITXOR BIT_XOR exprBITAND
               | exprBITAND
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITAND(p):
    '''
    exprBITAND : exprBITAND BIT_AND exprEQ
               | exprEQ
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprEQ(p):
    '''
    exprEQ : exprEQ EQ exprRELOP
           | exprEQ NE exprRELOP
           | exprRELOP
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprRELOP(p):
    '''
    exprRELOP : exprRELOP relop exprSHIFT
              | exprSHIFT
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_relop(p):
    '''
    relop : LE
          | LT
          | GE
          | GT
    '''
    p[0] = p[1]


def p_exprSHIFT(p):
    '''
    exprSHIFT : exprSHIFT L_SHIFT exprOP
              | exprSHIFT R_SHIFT exprOP
              | exprOP
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprOP(p):
    '''
    exprOP : exprOP PLUS term
         | exprOP MINUS term
         | term
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_term(p):
    '''
    term : term MULTIPLY factor
         | term DIVIDE factor
         | term MOD factor
         | factor
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_factor(p):
    '''
    factor : NOT factor
           | PLUS factor
           | MINUS factor
           | PLUS_PLUS factor
           | MINUS_MINUS factor
           | brace
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


def p_brace(p):
    '''
    brace  : L_PAREN expr R_PAREN
           | brace PLUS_PLUS
           | brace MINUS_MINUS
           | INT_NUM
           | FLOAT_NUM
           | ID
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


'''
def p_error(p):
    print('ERROR!!')'''

lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
    # file = "C:/Users/KR/PycharmProjects/Capstone/main/input_files/inp1.txt"

except:
    print('No arguments')


# ----------------------------------------------loop unrolling-------------------------------------------------------

def for_unroll_validate(tup):
    condition = tup[1]
    output = []
    # print(condition)
    if (type(condition[2][2]) == int and condition[2][2] <= 35):  # full unrolling
        solve(0, len(tup[2]), tup[2], output)
        unrolled = for_full_unroll(output, condition)
        res = (unrolled)
    else:
        solve(0, len(tup[2]), tup[2], output)
        unrolled = for_partial_unroll(output, condition)
        res = (tup[0], tup[1], unrolled)
    return res


def for_full_unroll(block, condition):
    block.pop(0)
    block.pop()
    res = []
    find_int(0, len(condition), condition, res)
    # print(res)
    return block * (abs(res[0][0] - res[1][0]))


def for_partial_unroll(block, condition):
    block.pop(0)
    block.pop()
    res = []
    find_int(0, len(condition), condition, res)
    total = abs(res[0][0] - res[1][0])
    factor = 0.5
    unroll_count = int(total * factor)
    # print(total,unroll_count)
    # print(res)
    # print(condition[2][res[1][-1]])
    condition[2][res[1][-1]] = total // unroll_count + res[0][0]
    # = res[1]//unroll_count
    extra = total % unroll_count
    return ['{'] + block * unroll_count + ['}'] + block * extra


def while_unroll_validate(tup):
    print(tup)
    # condition = tup[1]
    # output = []
    # print(condition)
    # if(type(condition[2][2])==int and condition[2][2] <= 35): # full unrolling
    #     solve(0,len(tup[2]),tup[2],output)
    #     unrolled = for_full_unroll(output, condition)
    #     res = (unrolled)
    # else:
    #     solve(0,len(tup[2]),tup[2],output)
    #     unrolled = for_partial_unroll(output, condition)
    #     res = (tup[0],tup[1],unrolled)
    return tup


# ----------------------------------------------loop unrolling-------------------------------------------------------


# ----------------------------------------------code generator ------------------------------------------------------


def solve(i, n, l, output_prg):
    if (i == n):
        return
    elif (type(l[i]) is str):
        if (l[i] == 'int' or l[i] == 'float'):
            output_prg += [l[i], ' ']
        else:
            output_prg += [l[i]]
        solve(i + 1, n, l, output_prg)
    elif (type(l[i]) is int):
        output_prg += [str(l[i])]
        solve(i + 1, n, l, output_prg)

    elif (type(l[i]) is tuple or type(l[i]) is list):
        solve(0, len(l[i]), l[i], output_prg)
        solve(i + 1, n, l, output_prg)


def find_int(i, n, l, res=[]):
    # print(l,i,level)
    if (i == n):
        return
    if (type(l[i]) is int):
        res.append([l[i], i])
    elif (type(l[i]) is list):
        find_int(0, len(l[i]), l[i], res)
    find_int(i + 1, n, l, res)


# ------------------------------------code generator -----------------------------------------------------------------------


# ------------------------------------IO handling --------------------------------------------------------------------------

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z = parser.parse(lines)

print("AST:")
print(z)
print()
print()
output_prg = []
solve(0, len(z), z, output_prg)
# print(output_prg)
print("generated code")
print("".join(output_prg))

# ----------------------------------IO handling -----------------------------------------------------------------------------
