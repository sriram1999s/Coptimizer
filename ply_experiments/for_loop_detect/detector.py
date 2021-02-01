from ply.lex import lex
from ply.yacc import yacc
import sys

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

datatype = ['INT', 'FLOAT']

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'L_SHIFT', 'R_SHIFT', 'AND', 'OR', 'XOR', 'MOD','PLUS_PLUS','MINUS_MINUS']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWERBRACE', 'R_FLOWERBRACE', 'SEMICOLON']

statements = ['FOR', 'WHILE']

tokens = datatype + bin_op + rel_op + delimiters + statements + ['ID', 'TYPE', 'NEWLINE']


# --------------------------------lexer------------------------------------ #

''' regular expressions defined here '''

# binary operators

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\\'
t_L_SHIFT = r'<<'
t_R_SHIFT = r'>>'
t_AND = r'&'
t_OR = r'\|'
t_XOR = r'\^'
t_MOD = r'%'
t_PLUS_PLUS=r'\+\+'
t_MINUS_MINUS=r'\-\-'

# relational operators

t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_EQ = r'=='

# assignment (had to be after relop)

t_ASSIGN = r'='

# delimiters

t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_FLOWERBRACE = r'\{'
t_R_FLOWERBRACE = r'\}'
t_SEMICOLON = r';'

# new NEWLINE

# t_NEWLINE = '\n'

t_ignore = ' \t'

# while
def t_WHILE(t):
    r'while'
    return t

# for

def t_FOR(t):
    r'for'
    return t

# float

def t_FLOAT(t):
    r'\d+\.\d+'
    return t

# int

def t_INT(t):
    r'\d+'
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

# def t_newline(t):
#     r'\n+'
#     pass
# --------------------------------parser------------------------------------ #

# defining precedence of operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

# detector

def p_detector(p):
    '''
    detector : for_loop
    '''
    print('loop detected')
    print(p[1])

''' grammer declared here '''

# statement
def p_statement(p):
    '''
    statement : var_assign SEMICOLON
              | expression SEMICOLON
              | expression_unary SEMICOLON
              | while_loop
              | for_loop
              | declaration SEMICOLON
              | SEMICOLON
    '''
    p[0] = p[1]

def p_statement_multiple(p):
    '''
    statement_multiple : statement_multiple statement
    '''
    p[0] = p[1] + [p[2]]

def p_statement_single(p):
    '''
    statement_multiple : statement
    '''
    p[0] = [p[1]]


# block

def p_block(p):
    '''
    block : L_FLOWERBRACE statement_multiple R_FLOWERBRACE
    '''
    p[0] = p[2]

# while

def p_while_loop(p):
    '''
    while_loop : WHILE condition block
               | WHILE condition statement
    '''
    p[0] = (p[1], p[2], p[3])

# for

def p_for_loop(p):
    '''
    for_loop : FOR for_condition block
             | FOR for_condition statement
    '''
    p[0] = (p[1], p[2], p[3])


# for condition

def p_for_condition(p):
    '''
    for_condition : L_PAREN var_assign SEMICOLON expression relop expression SEMICOLON var_assign R_PAREN
                  | L_PAREN declaration SEMICOLON expression relop expression SEMICOLON expression R_PAREN
    '''
    p[0] = (p[2], p[4], p[6])
# condition

def p_condition(p):
    '''
    condition : L_PAREN expression relop expression R_PAREN
    '''
    p[0] = (p[3], p[2], p[4])

# relop

def p_relop(p):
    '''
    relop : LE
          | LT
          | GE
          | GT
          | NE
          | EQ
    '''
    p[0] = p[1]



# declaration

def p_declaration(p):
    '''
    declaration : TYPE ID
                | TYPE var_assign
    '''
    p[0]=('declaring',p[1],p[2])

# assignment

def p_var_assign(p):
    '''
    var_assign : ID ASSIGN expression
    '''
    p[0] = (p[2], p[1], p[3])


# expression

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression L_SHIFT expression
               | expression R_SHIFT expression
               | expression MOD expression
               | expression XOR expression
               | expression AND expression
               | expression OR expression
    '''
    p[0] = (p[2], p[1], p[3])

# expression_unary

def p_expression_unary(p):
    '''
    expression_unary : post
                     | pre
    '''
    p[0] = p[1]

# post
def p_post(p):
    '''
    post : ID PLUS_PLUS
         | ID MINUS_MINUS
    '''
    p[0] = (p[2], p[1])

# pre
def p_pre(p):
    '''
    pre : PLUS_PLUS ID
        | MINUS_MINUS ID
    '''
    p[0] = (p[1], p[2])

# expressions

def p_expression_type(p):
    '''
    expression : INT
               | FLOAT
    '''
    # print('here2')
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : ID
    '''
    p[0] = p[1]

# lambda

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# error

# def p_error(p):
#     print('ERROR!!')


lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except :
    print('No arguments')

lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
    print(parser.parse(lines))

# while True:
#     try:
#         s = input()
#     except EOFError:
#         break
#     print(parser.parse(s))
