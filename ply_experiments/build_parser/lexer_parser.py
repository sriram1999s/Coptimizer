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

t -----> lexer object
p -----> production object

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


#--------------------------------------------PARSER-----------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------

from ply.yacc import yacc

def p_multiple_statements(p):
    '''
    statements : statements statement
    '''
    p[0] = p[1] + [p[2]]
    
def p_single_statements(p):
    '''
    statements : statement
    '''
    p[0]=[p[1]]
    
def p_assignment_statement(p):
    '''
    statement : VAR_NAME EQUALS expr
    '''
    p[0]=('assigning',p[1],p[2],p[3])
    
def p_expr_binop(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
         | expr TIMES expr
    	 | expr DIVIDE expr
     	 | expr L_SHIFT expr
         | expr R_SHIFT expr
         | expr AND expr
         | expr OR expr
         | expr XOR expr
         | expr MOD expr
    '''
    p[0]=(p[1],p[2],p[3])

def p_expr_int(p):
    '''
    expr : INT
    '''
    p[0] = ('integer',p[1])
    
def p_expr_name(p):
    '''
    expr : VAR_NAME
    '''
    p[0] = ('var_name',p[1])

# define rules for the parsers to follow in case of shift/reduce conflicts
precedence = (('left','PLUS','MINUS'),('left','TIMES','DIVIDE'))
    
#initializing the lexer and parser (Note that parser will not work without initializaing the lexer because it does not know where to find the lexer
lexer=lex()
parser=yacc()

print(parser.parse("a = 1*3 - 7"))
    
