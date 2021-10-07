from ply.lex import lex
import re

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

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'L_SHIFT', 'R_SHIFT', 'AND', 'OR', 'MOD','PLUS_PLUS','MINUS_MINUS','ARROW','DOT']

logic = ['BIT_OR', 'BIT_AND', 'BIT_XOR']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

assignment = ['ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'MOD_ASSIGN', 'L_SHIFT_ASSIGN', 'R_SHIFT_ASSIGN']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWBRACE', 'R_FLOWBRACE', 'SEMICOLON','COMMA','L_SQBRACE','R_SQBRACE']

statements = ['FOR', 'WHILE', 'IF', 'ELSE']

unary = ['NOT']

extra = ['ID', 'TYPE', 'STRING' , 'HASH', 'INCLUDE','HEADER_FILE','CHAR','TYPEDEF']

comment = ['MULTILINE_COMMENT','TAGGED_DS','LINEAR_SEARCH_BEGIN', 'LINEAR_SEARCH_END', 'POWER_OF_2_BEGIN', 'POWER_OF_2_END', 'COUNT_SET_BITS_BEGIN', 'COUNT_SET_BITS_END', 'UNIQUE_CHARACTERS_BEGIN', 'UNIQUE_CHARACTERS_END']

jump = ['RETURN']

tokens = numbers + bin_op + logic + rel_op + assignment + delimiters + statements + unary + extra + jump + comment


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
t_R_FLOWBRACE = r'\}' # defined later
t_L_SQBRACE = r'\['
t_R_SQBRACE = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_HASH = r'\#'


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
t_PLUS_PLUS=r'\+\+'
t_MINUS_MINUS=r'\-\-'
t_ARROW = r'->'
t_DOT = r'\.'

# logical operators

t_BIT_AND = r'\&'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'

# flow brace


def t_RETURN(t):
    r'return'
    return t

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
    r'\d+'
    t.value = int(t.value)
    return t

# string

def t_STRING(t):
    r'\".*?\"'
    return t

# types

def t_TYPE(t):
    r'(int|float|void|double|bool|char|struct\s+[A-Za-z_][A-Za-z_0-9]*)\s*\**'
    # #t.value.replace(' ','')
    res=''
    if(not t.value.startswith('struct')):
        for i in t.value:
            if(i!=' '):
                res+=i
        t.value = res

    else:
        m = re.match(r'(struct\s+[A-Za-z_][A-Za-z_0-9]*?\s)',t.value)
        res = m.group(1)
        start_ind = m.span()[-1] + 1
        for i in range(start_ind,len(t.value)):
            if(t.value[i]!=' '):
                res+=t.value[i]
        t.value = res

    # if(t.value[0:3]=='int'):
    #     print("t.value: ",t.value,"magan",sep = '')
    return t

#include

def t_INCLUDE(t):
    r'include'
    return t



def t_TAGGED_DS(t):
    r'/\*data-structure:.*?\*/'
    return t

def t_LINEAR_SEARCH_BEGIN(t):
    r'/\*linear-search-begin\*/'
    return t

def t_LINEAR_SEARCH_END(t):
    r'/\*linear-search-end\*/'
    return t

def t_POWER_OF_2_BEGIN(t):
    r'/\*power-of-2-begin\*/'
    return t

def t_POWER_OF_2_END(t):
    r'/\*power-of-2-end\*/'
    return t

def t_COUNT_SET_BITS_BEGIN(t):
    r'/\*count-set-bits-begin\*/'
    return t

def t_COUNT_SET_BITS_END(t):
    r'/\*count-set-bits-end\*/'
    return t

def t_UNIQUE_CHARACTERS_BEGIN(t):
    r'/\*unique-characters-begin\*/'
    return t

def t_UNIQUE_CHARACTERS_END(t):
    r'/\*unique-characters-end\*/'
    return t

# multiline comment
def t_MULTILINE_COMMENT(t):
    r'/\*.*?\*/'
    return t

# identifiers

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# HEADER_FILE

def t_HEADER_FILE(t):
    r'<.+?\..>'
    return t

def t_CHAR(t):
    '\'.\''
    return t

def t_TYPEDEF(t):
    'typedef'
    return t

# error

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)
