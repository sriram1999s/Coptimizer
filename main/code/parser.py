from lexer import *
from ply.yacc import yacc

from regenerator import *
from loop_unrolling import *
from collections import defaultdict

symbol_table = defaultdict(lambda:'galeej')
# --------------------------------parser------------------------------------ #

# defining precedence of operators
# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULTIPLY', 'DIVIDE')
# )

# start = 'start'
def p_start(p):
    '''
    start : multiple_statements
    '''
    for i in symbol_table:
        print(f"{i}------->{symbol_table[i]}")
    p[0] = p[1]

def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''
    if(len(p)==3):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

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
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]

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
        if(p[1] == 'for'):
            print("for detected")
            operators = []
            find_operator(0, len(p[2][-2]), p[2][-2], operators)
            ids = set()
            find_id(0, len(p[2][-2]), p[2][-2], ids)
            p[0] = for_unroll_validate([p[1], p[2], p[3]], operators, ids)
        else:
            print("while detected")
            p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]


def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    p[0] = [p[1],p[2],p[3]]

def p_for_condition(p):
    '''
    for_condition : L_PAREN declaration expr SEMICOLON expr R_PAREN
                  | L_PAREN expr SEMICOLON expr SEMICOLON expr R_PAREN
    '''
    if(len(p) == 7):
        p[0] = [p[1],p[2],p[3],p[4],p[5],p[6]]
    else :
        p[0] = [p[1],p[2],p[3],p[4],p[5],p[6],p[7]]

def p_multi_declaration(p):
    '''
    multi_declaration : multi_declaration ID COMMA
    		      | multi_declaration ID ASSIGN expr COMMA
		      | ID COMMA
    		      | ID ASSIGN expr COMMA
    '''
    if(len(p)==3):
        p[0]=[p[1],p[2]]
    elif(len(p)==4):
        p[0]=p[1]+[p[2],p[3]]
    elif(len(p)==6):
        p[0]=p[1]+[p[2],p[3],p[4],p[5]]
    else:
        p[0]=[p[1],p[2],p[3],p[4]]


def p_stop(p):
     '''
     stop : ID SEMICOLON
	      | ID ASSIGN expr SEMICOLON
     '''
     if(len(p)==3):
         p[0] = [p[1],p[2]]
     else:
         p[0] = [p[1],p[2],p[3],p[4]]


def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
		        | TYPE multi_declaration stop
    '''
    if(type(p[2])==str and p[3] == '='):
        global level
        global level_str
        global symbol_table
        print(p[2],p[4])
        symbol_table[p[2] + '_'.join(level_str)] = p[4]
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    if(len(p)==5):
        p[0] = [p[1], p[2], p[3], p[4]]
    if(len(p)==6):
        p[0] = [p[1], p[2], p[3], p[4], p[5]]

def p_block(p):
    '''
    block : L_FLOWBRACE multiple_statements R_FLOWBRACE
    '''
    p[0] = [p[1], p[2], p[3]]
    print(p[0])

def p_simple(p):
    '''
    simple : expr SEMICOLON
           | declaration
           | SEMICOLON
	       | function
	       | function_call
	       | RETURN ID SEMICOLON
       	       | RETURN INT_NUM SEMICOLON
	       | RETURN function_call
    '''
    if(len(p)==3):
        p[0] = [p[1],p[2]]
    elif(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    else:
        p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = []


def p_function_call(p):
    '''
    function_call : ID L_PAREN call_params R_PAREN SEMICOLON
    '''
    if(len(p) == 6):
        p[0] = [p[1], p[2], p[3], p[4], p[5]]

def p_call_params(p):
    '''
    	call_params : empty
		            | yes_call_params end_call_params
		            | end_call_params
    '''
    if(len(p) == 3):
        p[0] = p[1] + [p[2]]
    elif(len(p) == 2):
        p[0] = p[1]

def p_yes_call_params(p):
    '''
    yes_call_params : yes_call_params expr COMMA
		            | expr COMMA
    '''
    if(len(p)==3):
        p[0] = [p[1],p[2]]
    else:
        p[0] = p[1] + [p[2],p[3]]

def p_end_call_params(p):
    '''
    end_call_params : expr
    '''
    p[0] = p[1]


def p_yes_dec_params(p):
    '''
    yes_dec_params : yes_dec_params TYPE ID COMMA
    		   | yes_dec_params TYPE COMMA
		   | yes_dec_params TYPE ID ASSIGN NUM COMMA
                   | TYPE ID COMMA
   		   | TYPE COMMA
		   | TYPE ID ASSIGN NUM COMMA
    '''
    if (len(p) == 5):
        p[0] = p[1] + [p[2], p[3], p[4]]
    elif (len(p) == 4):
        p[0] = [p[1], p[2],p[3]]
    elif (len(p) == 7):
        p[0] = [p[1],p[2],p[3],p[4],p[5],p[6]]
    elif(len(p)==3):
        p[0] = [p[1],p[2]]
    else:
        p[0] = [p[1],p[2],p[3],p[4],p[5]]


def p_end_dec_params(p):
    '''
    end_dec_params : TYPE ID
		   | TYPE ID ASSIGN NUM
		   | TYPE
    '''
    if(len(p)==3):
        p[0] = [p[1], p[2]]
    elif(len(p)==5):
        p[0] = [p[1],p[2],p[3],p[4]]
    else:
        p[0] = p[1]


def p_dec_params(p):
    '''
    dec_params : empty
	       | yes_dec_params end_dec_params
	       | end_dec_params
    '''
    if (len(p) == 3):
        p[0] = [p[1],p[2]]
    elif(len(p)==2):
        p[0] = p[1]


def p_function(p):
    '''
    function : TYPE ID L_PAREN dec_params R_PAREN function_2
    '''
    p[0] = [p[1],p[2],p[3],p[4],p[5],p[6]]

def p_function_2(p):
    '''
    function_2 : SEMICOLON
    	       | block
    '''
    p[0]=[p[1]]

# def p_parameters(p):
#     '''
#     parameters : parameters TYPE ID COMMA stop
# 	       | stop
#     '''
#     if(len(p)==2):
#         p[0]=(p[1])
#     else:
#         p[0] = ((p[1]),p[2],p[3],p[4],p[5])

# def p_stop(p):
#     '''
#     stop : TYPE ID
#     '''
#     p[0] = (p[1],p[2])

def p_expr(p):
    '''
    expr : expr assignment exprOR
         | expr assignment ID L_PAREN call_params R_PAREN
         | exprOR
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    elif(len(p)==7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    else :
        p[0] = p[1]

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
    p[0] = p[1]

def p_exprOR(p):
    '''
    exprOR : exprOR OR exprAND
           | exprAND
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    else :
        p[0] = p[1]

def p_exprAND(p):
    '''
    exprAND : exprAND AND exprBITOR
            | exprBITOR
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    else :
        p[0] = p[1]

def p_exprBITOR(p):
    '''
    exprBITOR : exprBITOR BIT_OR exprBITXOR
              | exprBITXOR
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    else :
        p[0] = p[1]

def p_exprBITXOR(p):
    '''
    exprBITXOR : exprBITXOR BIT_XOR exprBITAND
               | exprBITAND
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    else :
        p[0] = p[1]

def p_exprBITAND(p):
    '''
    exprBITAND : exprBITAND BIT_AND exprEQ
               | exprEQ
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    else :
        p[0] = p[1]

def p_exprEQ(p):
    '''
    exprEQ : exprEQ EQ exprRELOP
           | exprEQ NE exprRELOP
           | exprRELOP
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    else :
        p[0] = p[1]

def p_exprRELOP(p):
    '''
    exprRELOP : exprRELOP relop exprSHIFT
              | exprSHIFT
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    else :
        p[0] = p[1]

def p_relop(p):
    '''
    relop : LE
          | LT
          | GE
          | GT
    '''
    p[0] = p[1]
def p_exprSHIFT(p):
    '''
    exprSHIFT : exprSHIFT L_SHIFT exprOP
              | exprSHIFT R_SHIFT exprOP
              | exprOP
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    else :
        p[0] = p[1]

def p_exprOP(p):
    '''
    exprOP : exprOP PLUS term
         | exprOP MINUS term
         | term
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
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
        p[0] = [p[1],p[2],p[3]]
    else :
        p[0] = p[1]

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
        p[0] = [p[1], p[2]]
    else :
        p[0] = p[1]

def p_brace(p):
    '''
    brace  : L_PAREN expr R_PAREN
           | brace PLUS_PLUS
           | brace MINUS_MINUS
           | NUM
           | ID
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    elif(len(p)==3):
        p[0] = [p[1], p[2]]
        print("brace",p[1],p[2])
    else:
        p[0] = p[1]


def p_NUM(p):
    '''
    NUM : INT_NUM
	| FLOAT_NUM
    '''
    p[0] = p[1]

# def p_ident(p):
#     '''
#         ident : ID
#               | ID ASSIGN function_call
#     '''
#     if(len(p)==2):
#         p[0] = p[1]
#     else :
#         p[0] = [p[1], p[2], p[3]]
#def p_error(p):
  # print('ERROR!!')
