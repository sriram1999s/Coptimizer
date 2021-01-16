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

tokens=['NAME','NUMBER','PLUS','MINUS','EQUALS','TIMES','DIVIDE','LPAREN','RPAREN','PRINT']

t_ignore=' \t'
t_PLUS=r'\+'
t_MINUS=r'-'
t_DIVIDE=r'/'
t_TIMES=r'\*'
t_EQUALS=r'='



def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if(t.value=='print'):
        t.type='PRINT'
    return t
    
t_LPAREN=r'\('
t_RPAREN=r'\)'


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

lexer=lex()

lexer.input("print(x)")

for tok in lexer:
    print(tok)


