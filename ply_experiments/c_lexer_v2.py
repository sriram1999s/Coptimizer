from ply.lex import lex
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

P.S: Try to stick to a single convention
'''

# Segregate the tokens and define please

datatypes = ['INT', 'FLOAT', 'DOUBLE']

operators = ['PLUS', 'MINUS', 'EQUALS', 'TIMES', 'DIVIDE', 'L_SHIFT', 'R_SHIFT', 'AND', 'OR', 'XOR', 'MOD','PLUS_PLUS','MINUS_MINUS']

relational_operators = ['LT', 'GT', 'LE', 'GE', 'NE', 'EQ']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWERBRACE', 'R_FLOWERBRACE', 'SEMICOLON','LBRACKET','RBRACKET','COLON','PERIOD']

tokens = datatypes + operators + relational_operators + delimiters + ['VAR_NAME', 'KEY_WORD']

t_ignore = r' \t'

# operators

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_EQUALS = r'='
t_L_SHIFT = r'<<'
t_R_SHIFT = r'>>'
t_AND = r'&'
t_OR = r'\|'
t_XOR = r'\^'
t_MOD = r'%'
t_PLUS_PLUS=r'\+\+'
t_MINUS_MINUS=r'\-\-'

# relational_operators

t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_EQ = r'=='

# delimiters
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_FLOWERBRACE = r'\{'
t_R_FLOWERBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]' 
t_SEMICOLON = r';'
t_PERIOD = r'\.'
t_COLON = r'\:'



def t_KEY_WORD(t):
    r'int|float|double|while|for'
    return t


def t_VAR_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if (t.value == 'printf'):
        t.type = 'PRINTF'
    return t


def t_FLOAT(t):
    r'\d+\.\d+'
    return t


def t_INT(t):
    r'\d+'
    return t


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


def tokenize():
    in_file=sys.argv[1]
    lines=""
    for line in open(in_file,"r"):
        lines+=line.strip('\n')
    print(lines)
    lexer = lex()
    lexer.input(lines)
    for tok in lexer:
        print(tok)

tokenize()
