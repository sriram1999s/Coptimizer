from ply.lex import lex
from ply.yacc import yacc
import sys

''' defining tokens '''

datatype = ['INT']

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWERBRACE', 'R_FLOWERBRACE', 'SEMICOLON']

statements = ['FOR', 'WHILE']

tokens = datatype + bin_op + rel_op + delimiters + statements + ['ID', 'TYPE']


# --------------------------------lexer------------------------------------ #

''' regular expressions defined here '''

# binary operators

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\\'

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

t_ignore = ' \t'

# while
def t_WHILE(t):
    r'while'
    return t

# for

def t_FOR(t):
    r'for'
    return t

# int

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# types

def t_TYPE(t):
    r'int'
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
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

# entire program

def p_detector(p):
    '''
    detector : statement
             | empty
    '''
    print(p[1])

# statement
def p_statement(p):
    '''
    statement : var_assign SEMICOLON
              | expression SEMICOLON
              | while_loop
    '''
    p[0] = p[1]

# while

def p_while_loop(p):
    '''
    while_loop : WHILE condition block
    '''
    p[0] = (p[1], p[2], p[3])

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
# block

def p_block(p):
    '''
    block : L_FLOWERBRACE statement R_FLOWERBRACE
    '''
    p[0] = p[2]

# assignment

def p_var_assign(p):
    '''
    var_assign : ID ASSIGN expression
    '''
    p[0] = (p[2], p[1], p[3])

# lambda

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# expression

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

# expressions

def p_expression_type(p):
    '''
    expression : INT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : ID
    '''
    p[0] = p[1]

def p_error(p):
    print('ERROR!!')


lexer = lex()
parser = yacc()

while True:
    try:
        s = input()
    except EOFError:
        break
    parser.parse(s)
