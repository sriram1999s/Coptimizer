from ply.lex import lex

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

jump = ['RETURN']

tokens = numbers + bin_op + logic + rel_op + assignment + delimiters + statements + unary + extra + jump

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


# return

def t_RETURN(t):
    r'return'
    print('in lexer return')
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
