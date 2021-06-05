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

P.S: Try to stick to a single convention
'''

# Segregate the tokens and define please

datatypes=['INT','FLOAT','DOUBLE']

binary_operators=['PLUS','MINUS','EQUALS','TIMES','DIVIDE','LSHIFT','RSHIFT','AND','OR','XOR','MOD']

delimiters=['LPAREN','RPAREN','SEMICOLON']

tokens=datatypes+binary_operators+delimiters+['VAR_NAME','NUMBER']

t_ignore=' \t'

#binary_operators

t_PLUS=r'\+'
t_MINUS=r'-'
t_DIVIDE=r'/'
t_TIMES=r'\*'
t_EQUALS=r'='
t_LSHIFT=r'<<'
t_RSHIFT=r'>>'
t_AND=r'&'
t_OR=r'\|'
t_XOR=r'\^'
t_MOD=r'%'

#delimiters
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_SEMICOLON=r';'



def t_VAR_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if(t.value=='print'):
        t.type='PRINT'
    if(t.value=='int'):
        t.type='INT'
    if(t.value=='float'):
        t.type='FLOAT'
    if(t.value=='double'):
        t.type='DOUBLE'
    return t
    

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

lexer=lex()

lexer.input("int x = (5|3)*(7>>2)/(8<<1)-(3^4);")

for tok in lexer:
    print(tok)


