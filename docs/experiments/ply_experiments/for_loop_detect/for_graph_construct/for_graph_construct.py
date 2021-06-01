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

numbers = ['INT_NUM', 'FLOAT_NUM']

bin_op = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'L_SHIFT', 'R_SHIFT', 'AND', 'OR', 'MOD','PLUS_PLUS','MINUS_MINUS']

logic = ['BIT_OR', 'BIT_AND', 'BIT_XOR']

rel_op = ['LT', 'LE', 'GT', 'GE', 'NE', 'EQ']

assignment = ['ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'MOD_ASSIGN', 'L_SHIFT_ASSIGN', 'R_SHIFT_ASSIGN']

delimiters = ['L_PAREN', 'R_PAREN', 'L_FLOWBRACE', 'R_FLOWBRACE', 'SEMICOLON']

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

# --------------------------------parser------------------------------------ #

# defining precedence of operators
# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULTIPLY', 'DIVIDE')
# )

# start = 'start'

from collections import defaultdict
graph = defaultdict(lambda:[])
level = 0
level_str = []

def p_start(p):
    '''
    start : multiple_statements
    '''
    #print(p[1])
    p[0] = p[1]

def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''
    if(len(p)==3):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

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
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], (p[2], p[3]), p[4], p[5])

def p_closed(p):
    '''
    closed : simple
           | block
           | IF condition closed ELSE closed
           | WHILE condition closed
           | FOR for_condition closed
    '''
    if(len(p)==2):
        p[0] = p[1]
    elif(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], (p[2], p[3]), p[4], p[5])

def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    global level
    global level_str
    if(len(level_str)>0 and level==int(level_str[-1])):
        level=1
    level_str.append(str(level))
    p[0] = (p[1],p[2],p[3])

def p_for_condition(p):
    '''
    for_condition : L_PAREN declaration expr SEMICOLON expr R_PAREN
    '''
    global level
    global level_str
    if(level==0):
        level+=1
    if(len(level_str)>0 and level==int(level_str[-1])):
        level=1
    level_str.append(str(level))
    p[0] = (p[1],p[2],p[3],p[4],p[5],p[6])

def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
    '''
    global level
    global graph
    global level_str
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    if(level>0 and len(level_str)>0):
        #print(type(p[0]),p[0])
        #print(level_str)
        #print('for'+'_'.join(level_str))
        #print(level,level_str)
        graph['for'+'_'.join(level_str)].append(p[0])

def p_block(p):
    '''
    block : L_FLOWBRACE multiple_statements R_FLOWBRACE
    '''
    global level
    global level_str
    level=int(level_str.pop())+1
    p[0] = (p[1], p[2], p[3])

def p_simple(p):
    '''
    simple : expr SEMICOLON
           | declaration
           | SEMICOLON
    '''
    if(len(p)==3):
        p[0] = (p[1],p[2])
    else:
        p[0] = (p[1])

def p_expr(p):
    '''
    expr : expr assignment exprOR
         | exprOR
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = (p[1])

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
    p[0] = (p[1])

def p_exprOR(p):
    '''
    exprOR : exprOR OR exprAND
           | exprAND
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = (p[1])

def p_exprAND(p):
    '''
    exprAND : exprAND AND exprBITOR
            | exprBITOR
    '''
    if(len(p)==4):
        p[0] = (p[2], p[1], p[3])
    else :
        p[0] = (p[1])

def p_exprBITOR(p):
    '''
    exprBITOR : exprBITOR BIT_OR exprBITXOR
              | exprBITXOR
    '''
    if(len(p)==4):
        p[0] = (p[1],p[2],p[3])
    else :
        p[0] = (p[1])

def p_exprBITXOR(p):
    '''
    exprBITXOR : exprBITXOR BIT_XOR exprBITAND
               | exprBITAND
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = (p[1])

def p_exprBITAND(p):
    '''
    exprBITAND : exprBITAND BIT_AND exprEQ
               | exprEQ
    '''
    if(len(p)==4):
        p[0] = (p[1],p[2],p[3])
    else :
        p[0] = (p[1])

def p_exprEQ(p):
    '''
    exprEQ : exprEQ EQ exprRELOP
           | exprEQ NE exprRELOP
           | exprRELOP
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = (p[1])
        
def p_exprRELOP(p):
    '''
    exprRELOP : exprRELOP relop exprSHIFT
              | exprSHIFT
    '''
    if(len(p)==4):
        p[0] = (p[1],p[2],p[3])
    else :
        p[0] = (p[1])
        
def p_relop(p):
    '''
    relop : LE
          | LT
          | GE
          | GT
    '''
    p[0] = (p[1])
def p_exprSHIFT(p):
    '''
    exprSHIFT : exprSHIFT L_SHIFT exprOP
              | exprSHIFT R_SHIFT exprOP
              | exprOP
    '''
    if(len(p)==4):
        p[0] = (p[1],p[2],p[3])
    else :
        p[0] = (p[1])

def p_exprOP(p):
    '''
    exprOP : exprOP PLUS term
         | exprOP MINUS term
         | term
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    else :
        p[0] = p[1]

def p_term(p):
    '''
    term : term MULTIPLY factor
         | term DIVIDE factor
         | term MOD factor
         | factor
    '''
    if(len(p)==4):
        p[0] = (p[1],p[2],p[3])
    else :
        p[0] = (p[1])

def p_factor(p):
    '''
    factor : NOT factor
           | PLUS factor
           | MINUS factor
           | PLUS_PLUS factor
           | MINUS_MINUS factor
           | brace
    '''
    if(len(p)==3):
        p[0] = (p[1], p[2])
    else :
        p[0] = (p[1])

def p_brace(p):
    '''
    brace  : L_PAREN expr R_PAREN
           | brace PLUS_PLUS
           | brace MINUS_MINUS
           | INT_NUM
           | FLOAT_NUM
           | ID
    '''
    if(len(p)==4):
        p[0] = (p[1], p[2], p[3])
    elif(len(p)==3):
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1])
        
def p_error(p):
    print('ERROR!!')


lexer = lex()
parser = yacc()

try:
    file = sys.argv[1]
except :
    print('No arguments')

#----------------------------------------------code generator ------------------------------------------------------



def solve(i,n,l,output_prg):
    if(i==n):
        return
    elif(type(l[i]) is str):
        if(l[i] == 'int' or l[i] == 'float'):
            output_prg+=[l[i],' ']
        else:
            output_prg+=[l[i]]
        solve(i+1,n,l,output_prg)
    elif(type(l[i]) is int):
        output_prg+=[str(l[i])]
        solve(i+1,n,l,output_prg)

    elif(type(l[i]) is tuple or type(l[i]) is list):
        for j in range(len(l[i])):
            if(type(l[i][j]) is tuple or type(l[i][j]) is list):
                solve(0,len(l[i][j]),l[i][j],output_prg)
            else:
                if(l[i][j]=='int' or l[i][j]=='float'):
                    output_prg+=[str(l[i][j]),' ']
                else:
                    output_prg+=[str(l[i][j])]
        solve(i+1,n,l,output_prg)



#------------------------------------code generator -----------------------------------------------------------------------


#------------------------------------IO handling --------------------------------------------------------------------------
    
lines = ""
with open(file) as f:
    for line in f:
        lines += line.strip('\n')
    lines.strip('\n')
z=parser.parse(lines)

#print("AST:")
#print(z)
#print()
#print()
output_prg=[]
solve(0,len(z),z,output_prg)
#print(output_prg)
print("generated code")
print("".join(output_prg))
print()
print()
for i in graph:
    print(f"{i}---->{graph[i]}")

#----------------------------------IO handling -----------------------------------------------------------------------------
