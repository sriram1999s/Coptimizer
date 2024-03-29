from lexer import *
from ply.yacc import yacc

from regenerator import *
from loop_unrolling import *
from symboltable import *
from function_inline import *
from collections import defaultdict
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
    #print('#printing symbol table....')
    for i in symbol_table:
        if(symbol_table[i] != 'garbage'):
            x_1212dfjhi2378 = 1
            #print(f"\t{i}------->{symbol_table[i]}")
    p[0] = p[1]

def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''
    if(len(p)==3):
        #print("p_multiple_statements :")
        #print("p[1] :",p[1])
        #print("p[2] :",p[2])
        p[0] = p[1] + [p[2]]
        '''if(type(p[1]) is list):
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1],p[2]]'''
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
        lookahead(0, len(p[3]), p[3])
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]
        lookahead(0, len(p[3]), p[3])
        lookahead(0, len(p[5]), p[5])

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
            #print("for detected\n")
            p[0] = for_unroll_validate([p[1], p[2], p[3]])
            lookahead(0, len(p[3]), p[3])
        else:
            #print("while detected\n")
            p[0] = [p[1], p[2], p[3]]
            lookahead(0, len(p[3]), p[3])
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]
        lookahead(0, len(p[3]), p[3])
        lookahead(0, len(p[5]), p[5])


def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    p[0] = [p[1],p[2],p[3]]

def p_for_condition(p):
    '''
    for_condition : L_PAREN simple simple expr R_PAREN
                  | L_PAREN simple simple R_PAREN
    '''
    if(len(p) == 6):
        p[0] = [p[1], p[2], p[3], p[4], p[5]]
    else:
        p[0] = [p[1], p[2], p[3], p[4]]

def p_multi_declaration(p):
    '''
    multi_declaration : multi_declaration ID COMMA
                      | multi_declaration MULTIPLY ID COMMA
    		          | multi_declaration ID ASSIGN expr COMMA
                      | multi_declaration MULTIPLY ID ASSIGN expr COMMA
		              | ID COMMA
    		          | ID ASSIGN expr COMMA
                      | MULTIPLY ID COMMA
                      | MULTIPLY ID ASSIGN expr COMMA
    '''
    if(len(p)==3):
        p[0]=[p[1],p[2]]
    elif(len(p)==4):
        if(p[1] == '*'):
            p[0]=[p[1],p[2],p[3]]
        else:
            p[0]=p[1]+[p[2],p[3]]
    elif(len(p)==5):
        p[0]=p[1]+[p[2],p[3],p[4]]
    elif(len(p)==6):
        if(p[1] == '*'):
            p[0] = [p[1],p[2],p[3],p[4],p[5]]
        else:
            p[0]=p[1]+[p[2],p[3],p[4],p[5]]
    elif(len(p)==7):
        p[0]=p[1]+[p[2],p[3],p[4],p[5],p[6]]
    else:
        p[0]=[p[1],p[2],p[3],p[4]]


def p_stop(p):
     '''
     stop : ID SEMICOLON
          | MULTIPLY ID SEMICOLON
	      | ID ASSIGN expr SEMICOLON
          | MULTIPLY ID ASSIGN expr SEMICOLON
     '''
     if(len(p)==3):
         p[0] = [p[1],p[2]]
     elif(len(p)==4):
         p[0] = [p[1], p[2], p[3]]
     elif(len(p)==5):
         p[0] = [p[1],p[2],p[3],p[4]]
     else:
         p[0] = [p[1],p[2],p[3],p[4],p[5]]

def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE MULTIPLY ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
                | TYPE MULTIPLY ID ASSIGN expr SEMICOLON
		        | TYPE multi_declaration stop
    			| TYPE ID L_SQBRACE index R_SQBRACE SEMICOLON
    			| TYPE ID L_SQBRACE index R_SQBRACE ASSIGN L_FLOWBRACE init_list R_FLOWBRACE SEMICOLON

    '''
    global level
    global level_str
    global symbol_table

    if(p[2] == "*"):
        search_string = '*' + p[3] + '_'.join(level_str)
        if(p[4] == '='):
            if(type(p[5]) == str):
                dynamic_string = '*' + p[5] + '_'.join(level_str)
                copy_level_str = level_str.copy()
                while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                    copy_level_str.pop()
                    dynamic_string = '*' + p[5] + '_'.join(copy_level_str)
                if(symbol_table[dynamic_string]!= 'garbage' and symbol_table[dynamic_string]!= 'declared'):
                    symbol_table[search_string ] = symbol_table[dynamic_string]
                else:
                    symbol_table[search_string] = p[5]
            else:
                temp = []
                solve(0, len(p[5]), p[5], temp)
                rhs = ''.join(temp).strip('&')
                dynamic_string = rhs + '_'.join(level_str)
                copy_level_str = level_str.copy()
                while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                    copy_level_str.pop()
                    dynamic_string = rhs + '_'.join(copy_level_str)
                if(symbol_table[dynamic_string]!='garbage' and symbol_table[dynamic_string]!='declared'):
                    if(re.search(r'(?:\d+\.\d+)|(?:\d+)|(?:".*?")|(?:\'.\')',str(symbol_table[dynamic_string]))):
                        symbol_table[search_string] = rhs
                    else:
                        symbol_table[search_string] = symbol_table[dynamic_string]
                else:
                    symbol_table[search_string] =  rhs

        elif(p[4] == ';'):
            symbol_table[search_string] = 'declared'

        if(symbol_table[search_string]!='garbage' and symbol_table[search_string]!='declared'):
            for var in symbol_table:
                if(symbol_table[var]==p[3]):
                    symbol_table[var] = symbol_table[search_string]

    elif(type(p[2])==str):
        if(p[3]== '='):
            search_string = p[2] + '_'.join(level_str)
            if(type(p[4])==int):
                symbol_table[search_string] = p[4]
            elif(type(p[4])==str and re.search(r'[A-Za-z_][A-Za-z_0-9]*',p[4])):
                dynamic_string = p[4] + '_'.join(level_str)
                copy_level_str = level_str.copy()
                while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                    copy_level_str.pop()
                    dynamic_string = p[4] + '_'.join(copy_level_str)
                if(symbol_table[dynamic_string]!='garbage' and symbol_table[dynamic_string]!='declared'):
                    symbol_table[search_string] = symbol_table[dynamic_string]
                else:
                    symbol_table[search_string] = p[4]
            else:
                symbol_table[search_string] = p[4]

            if(symbol_table[search_string]!='garbage' and symbol_table[search_string]!='declared'):
                for var in symbol_table:
                    if(symbol_table[var]==p[2]):
                        symbol_table[var] = symbol_table[search_string]



        elif( p[3] == ';'):
            symbol_table[p[2] + '_'.join(level_str)] = 'declared'

    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    if(len(p)==5):
        p[0] = [p[1], p[2], p[3], p[4]]
    if(len(p)==6):
        ''' deals with fn calls in declaration '''
        if(type(p[4]) is list and type(p[4][0]) is tuple):
            t = p[4][0]
            p[0] = [p[1],p[2],p[3],t[0],'(',t[1][2],')',p[5]]
            call_helper(p[0],t[0])
            p[0] = [(t[0], p[0][3:], "call", p[1], p[2])]
        else:
            p[0] = [p[1], p[2], p[3], p[4], p[5]]
        # #print("p_declaration : ",p[0])

    if(len(p)==7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    if(len(p)==11):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6] , p[7] , p[8] , p[9] , p[10]]

def p_init_list(p):
    '''
    init_list : expr COMMA init_list
    	      | expr
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    if(len(p)==2):
        p[0] = [p[1]]

def p_index(p):
    '''
    index : NUM
    	    | empty
    '''
    if(p[1]!=None):
        p[0] = p[1]

def p_block(p):
    '''
    block : left_flower multiple_statements right_flower
    '''
    p[0] = [p[1], p[2], p[3]]

def p_left_flower(p):
    '''
    left_flower : L_FLOWBRACE
    '''
    global level
    global level_str
    level = '%'
    level_str.append(level)
    p[0] = p[1]

def p_right_flower(p):
    '''
    right_flower : R_FLOWBRACE
    '''
    global level
    global level_str
    level_str.pop()
    p[0] = p[1]

def p_simple(p):
    '''
    simple : expr SEMICOLON
	       | header
           | declaration
           | SEMICOLON
	       | function
	       | RETURN expr SEMICOLON
           | RETURN SEMICOLON
    '''
    if(len(p)==3):
        # if(p[1] != "return"):
        #     # #print("Before err : ",list(p))
        #     # p[1].append(';') # FLAG
        #     p[0] = [p[1]]
        # else:
        #     p[0] = [p[1],p[2]]
        p[0] = [p[1],p[2]]
    elif(len(p)==4):
        # #print("p_simpleI :",p[2])
        if(type(p[2]) is list and type(p[2][0]) is tuple):
            t = p[2][0]
            p[0] = [p[1], t[0], '(',t[1][2], ')',';']
            call_helper(p[0], t[0])
            p[0] = [(t[0] , p[0][1:] , "call" , "ret" , "ret" ,"return")]
        else:
            p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]

def p_header(p):
    '''
    header : HASH INCLUDE STRING
	   | HASH INCLUDE HEADER_FILE
    '''
    p[0] = [p[1],p[2],p[3]+'\n']

def p_empty(p):
    'empty :'
    p[0] = []


def p_function_call(p):
    '''
    function_call : ID L_PAREN call_params R_PAREN
    '''
    # #print("function_call : ",list(p))
    p[0] = [p[1], p[2], p[3], p[4],';']
    call_helper(p[0],p[1])
    p[0] = [(p[1],p[0][0 : -1], 'call')]

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
                   | yes_dec_params TYPE MULTIPLY ID COMMA
    		       | yes_dec_params TYPE COMMA
                   | yes_dec_params TYPE MULTIPLY COMMA
		           | yes_dec_params TYPE ID ASSIGN NUM COMMA
                   | TYPE ID COMMA
                   | TYPE MULTIPLY ID COMMA
   		           | TYPE COMMA
                   | TYPE MULTIPLY COMMA
		           | TYPE ID ASSIGN NUM COMMA
    '''
    if (len(p) == 5):
        if(type(p[1])==str):
            p[0] = [p[1],p[2],p[3],p[4]]
        else:
            p[0] = p[1] + [p[2], p[3], p[4]]
    elif(len(p) == 6):
        p[0] = p[1] + [p[2], p[3], p[4], p[5]]
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
                   | TYPE MULTIPLY ID
                   | TYPE MULTIPLY
    '''
    if(len(p)==3):
        p[0] = [p[1], p[2]]
    elif(len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
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
    #print("\n\np_functionnnn :",p[6],"\n\n")
    if p[2] != 'main':
        if(p[6][0] != ';'):
            temp = inline_defn_helper(p[0],p[2])
            p[0] = [temp]

def p_function_2(p):
    '''
    function_2 : SEMICOLON
    	       | block
    '''
    p[0]=[p[1]]


def p_expr(p):
    '''
    expr : expr assignment exprOR
         | exprOR
    '''
    if(len(p) > 2 and type(p[1])==str):
        search_string = p[1] + "_".join(level_str)
        # #print("search_string : ", search_string)
        if(len(level_str) != 0):
            copy_level_str = level_str.copy()
            while( (symbol_table[search_string] == 'garbage' and symbol_table['*' + search_string] == 'garbage') and len(copy_level_str)>1):
                copy_level_str.pop()
                # #print("copy_level_str", copy_level_str)
                search_string = p[1] + "_".join(copy_level_str)
                # #print("search_string : ", search_string)
        # #print("* search", '*' + search_string , symbol_table['*' + search_string ])
        # #print("search",search_string , symbol_table[ search_string ])
        # #print("p[3]", p[3])
        if(type(p[3])==str and re.search(r'[A-Za-z_][A-Za-z_0-9]*',p[3])):
            if(symbol_table['*' + search_string ] == "garbage" ):
                # #print("here")
                dynamic_string = p[3] + '_'.join(level_str)
                copy_level_str = level_str.copy()
                while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                    copy_level_str.pop()
                    dynamic_string = p[3] + '_'.join(copy_level_str)
                if(symbol_table[dynamic_string]!='garbage' and symbol_table[dynamic_string]!='declared'):
                    symbol_table[search_string] = symbol_table[dynamic_string]
                else:
                    symbol_table[search_string] = p[3]
            else:
                dynamic_string = "*" + p[3] + '_'.join(level_str)
                copy_level_str = level_str.copy()
                while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                    copy_level_str.pop()
                    dynamic_string = "*" + p[3] + '_'.join(copy_level_str)
                if(symbol_table[dynamic_string]!='garbage' and symbol_table[dynamic_string]!='declared'):
                    symbol_table['*' + search_string ] = symbol_table[dynamic_string]
                else:
                    symbol_table['*' + search_string] = p[3]

        elif(symbol_table['*' + search_string ] != "garbage" and type(p[3])==list):
            temp = []
            solve(0, len(p[3]), p[3], temp)
            rhs = ''.join(temp).strip('&')
            dynamic_string = rhs + '_'.join(level_str)
            copy_level_str = level_str.copy()
            while(symbol_table[dynamic_string] == 'garbage' and len(copy_level_str)>1):
                copy_level_str.pop()
                dynamic_string = rhs + '_'.join(copy_level_str)
            if(symbol_table[dynamic_string]!='garbage' and symbol_table[dynamic_string]!='declared'):
                    if(re.search(r'(?:\d+\.\d+)|(?:\d+)|(?:".*?")|(?:\'.\')',str(symbol_table[dynamic_string]))):
                        symbol_table['*'+search_string] = rhs
                    else:
                        symbol_table['*'+search_string] = symbol_table[dynamic_string]
            else:
                symbol_table['*'+search_string] =  rhs
        else:
            symbol_table[search_string] = p[3]

        #for i in symbol_table:
         #   #print(f'{i}---->{symbol_table[i]}')


        if(symbol_table[search_string]!='garbage' and symbol_table[search_string]!='declared'):
            for var in symbol_table:
                if(symbol_table[var]==p[1]):
                    ##print(var,symbol_table[search_string])
                    symbol_table[var] = symbol_table[search_string]

        if(symbol_table['*'+search_string]!='garbage' and symbol_table['*'+search_string]!='declared'):
            for var in symbol_table:
                if(symbol_table[var]==p[1]):
                    symbol_table[var] = symbol_table['*'+search_string]

    if(len(p)==4):
        # #print("p_expr : ",p[3])
        if(type(p[3]) is list and type(p[3][0]) is tuple):
            t = p[3][0]
            p[0] = [p[1],p[2],t[0],'(',t[1][2],')']
            call_helper(p[0],t[0])
            p[0] = [ ( t[0] , p[0][2:] , "call" , p[1])]
        else:
            p[0] = [p[1], p[2], p[3]]
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
           | STRING
           | MULTIPLY ID
           | BIT_AND ID
           | ID
           | function_call
    	   | ID L_SQBRACE index R_SQBRACE
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    elif(len(p)==5):
        p[0] = [p[1], p[2], p[3],p[4]]
    elif(len(p)==3):
        p[0] = [p[1], p[2]]
    else:
        if(type(p[1]) is list and type(p[1][0]) is tuple):
            t = copy.deepcopy(p[1][0])
            t = list(flatten(t))
            if(t.count("call") > 1):
                remove_nested_calls(0,len(p[1]),p[1])
            del(t)
        p[0] = p[1]


def p_NUM(p):
    '''
    NUM : INT_NUM
	    | FLOAT_NUM
    '''
    p[0] = p[1]

def p_error(p):
    x_1212dfjhi2378 = 1
    #print(f"an error occurred ::: token {p} , char {p.value}")
