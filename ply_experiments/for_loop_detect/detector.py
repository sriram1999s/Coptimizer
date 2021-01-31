from ply.lex import lex
from ply.yacc import yacc
import sys

''' defining tokens '''

datatype = ['INT']

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWERBRACE', 'R_FLOWERBRACE', 'SEMICOLON']

statements = ['FOR']

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
def p_detector(p):
    '''
    detector : expression
             | empty
    '''
    print(p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_type(p):
    '''
    expression : INT
    '''
    p[0] = p[1]

lexer = lex()
parser = yacc()

while True:
    try:
        s = input()
    except EOFError:
        break
    parser.parse(s)
