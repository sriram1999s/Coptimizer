from lexer_file import *
from ply.yacc import yacc

from regenerator import *
from loop_unrolling import *
from function_inline import *

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
    p[0] = p[1]


def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''
    if (len(p) == 3):
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
    if (len(p) == 4):
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
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        if (p[1] == 'for'):
            print("for detected")
            # p[0] = [p[1],p[2],p[3]]
            p[0] = for_unroll_validate([p[1], p[2], p[3]])
        else:
            print("while detected")
            p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]


def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    p[0] = [p[1], p[2], p[3]]


def p_for_condition(p):
    '''
    for_condition : L_PAREN declaration expr SEMICOLON expr R_PAREN
                | L_PAREN expr SEMICOLON expr SEMICOLON expr R_PAREN
    '''
    if (len(p) == 7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]


def p_multi_declaration(p):
    '''
    multi_declaration : multi_declaration ID COMMA
    		      | multi_declaration ID ASSIGN expr COMMA
		      | ID COMMA
    		      | ID ASSIGN expr COMMA
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        p[0] = p[1] + [p[2], p[3]]
    elif (len(p) == 6):
        p[0] = p[1] + [p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4]]


def p_stop(p):
    '''
     stop : ID SEMICOLON
	      | ID ASSIGN expr SEMICOLON
     '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1], p[2], p[3], p[4]]


def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
                | TYPE ID ASSIGN function_call
		        | TYPE multi_declaration stop
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    elif (len(p) == 5):
        p[0] = [p[1], p[2], p[3], p[4]]
    else:
        p[0] = [p[1], p[2], p[3], p[4], p[5]]


def p_block(p):
    '''
    block : L_FLOWBRACE multiple_statements R_FLOWBRACE
    '''
    p[0] = [p[1], p[2], p[3]]


def p_simple(p):
    '''
    simple : expr SEMICOLON
           | declaration
           | SEMICOLON
	       | function
	       | function_call
	       | RETURN ID SEMICOLON
	       | RETURN INT_NUM SEMICOLON
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_empty(p):
    'empty :'
    p[0] = []


def p_function_call(p):
    '''
    function_call : ID L_PAREN call_params R_PAREN SEMICOLON
    '''
    # global pass_no
    if (len(p) == 6):
        p[0] = [p[1], p[2], p[3], p[4], p[5]]

    f0 = open("parse_track", 'r')
    pass_no = f0.read()
    f0.close()
    pass_no = int(pass_no)
    if pass_no == 1:
        if type(p[3]) is not list:
            p[3] = [p[3]]
        create_call_obj(p[1], p[3], None)
    if pass_no == 2:
        call = fn_call_obj_dict[p[1]].pop(0)
        if fn_defn_obj_dict[p[1]].inline_flag == 1:
            p[0] = inline("p_function_call", p[1], call.actual_arguments, None)


def p_call_params(p):
    '''
    	call_params : empty
		            | yes_call_params end_call_params
		            | end_call_params
    '''
    if (len(p) == 3):
        p[0] = p[1] + [p[2]]
    elif (len(p) == 2):
        p[0] = p[1]


def p_yes_call_params(p):
    '''
    yes_call_params : yes_call_params INT_NUM COMMA
    		    | yes_call_params ID COMMA
		    | INT_NUM COMMA
		    | ID COMMA
    '''
    if (len(p) == 0):
        p[0] = []
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1] + [p[2], p[3]]


def p_end_call_params(p):
    '''
    end_call_params : INT_NUM
		    | ID
    '''
    p[0] = p[1]


def p_yes_dec_params(p):
    '''
    yes_dec_params : yes_dec_params TYPE ID COMMA
                    | TYPE ID COMMA
    '''
    if (len(p) == 5):
        p[0] = p[1] + [p[2], p[3], p[4]]
    elif (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]


def p_end_dec_params(p):
    '''
    end_dec_params : TYPE ID
    '''
    p[0] = [p[1], p[2]]


def p_dec_params(p):
    '''
    dec_params : empty
	       | yes_dec_params end_dec_params
	       | end_dec_params
    '''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 2):
        p[0] = p[1]


def p_function(p):
    '''
    function : TYPE ID L_PAREN dec_params R_PAREN function_2
    '''
    # global pass_no
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    f0 = open("parse_track", 'r')
    pass_no = f0.read()
    pass_no = int(pass_no)
    if pass_no == 1 and p[2]!='main':
        create_defn_obj(p[1], p[2], p[4], p[6])
    elif pass_no == 2 and p[2]!='main':
        if fn_defn_obj_dict[p[2]].inline_flag == 1:
            p[0] = []
    f0.close()

def p_function_2(p):
    '''
    function_2 : SEMICOLON
    	       | block
    '''
    p[0] = [p[1]]


def p_expr(p):
    '''
    expr : expr assignment exprOR
         | expr assignment ID L_PAREN call_params R_PAREN
         | exprOR
    '''
    # global pass_no
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    elif(len(p) == 7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
        f0 = open("parse_track", 'r')
        pass_no = f0.read()
        f0.close()
        pass_no = int(pass_no)
        if pass_no == 1:
            create_call_obj(p[1], p[3], p[1][0])
        if pass_no == 2:
            call = fn_call_obj_dict[p[3]].pop(0)
            if call.inline_flag == 1:
                p[0] = inline("p_expr", p[3], p[5], p[1][0])
    # elif (len(p) == 8):
    #     p[0] = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]]
    #     f0 = open("parse_track", 'r')
    #     pass_no = f0.read()
    #     f0.close()
    #     pass_no = int(pass_no)
    #     if pass_no == 1:
    #         create_call_obj(p[1], p[3], p[1][0])
    #     if pass_no == 2:
    #         call = fn_call_obj_dict[p[3]].pop(0)
    #         if call.inline_flag == 1:
    #             p[0] = inline("p_expr", p[3], p[5], p[1][0])
    else:
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
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprAND(p):
    '''
    exprAND : exprAND AND exprBITOR
            | exprBITOR
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITOR(p):
    '''
    exprBITOR : exprBITOR BIT_OR exprBITXOR
              | exprBITXOR
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITXOR(p):
    '''
    exprBITXOR : exprBITXOR BIT_XOR exprBITAND
               | exprBITAND
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprBITAND(p):
    '''
    exprBITAND : exprBITAND BIT_AND exprEQ
               | exprEQ
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprEQ(p):
    '''
    exprEQ : exprEQ EQ exprRELOP
           | exprEQ NE exprRELOP
           | exprRELOP
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprRELOP(p):
    '''
    exprRELOP : exprRELOP relop exprSHIFT
              | exprSHIFT
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
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
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_exprOP(p):
    '''
    exprOP : exprOP PLUS term
         | exprOP MINUS term
         | term
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]


def p_term(p):
    '''
    term : term MULTIPLY factor
         | term DIVIDE factor
         | term MOD factor
         | factor
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
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
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


def p_brace(p):
    '''
    brace  : L_PAREN expr R_PAREN
           | brace PLUS_PLUS
           | brace MINUS_MINUS
           | INT_NUM
           | FLOAT_NUM
           | ID
    '''
    if (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


# def p_error(p):
#   print('ERROR!!')
