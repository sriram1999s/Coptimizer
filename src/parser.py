from lexer import *
from ply.yacc import yacc
from menu import *
from regenerator import *
from optimizations.loop_unrolling import *
from optimizations.symboltable import *
from optimizations.compile_time_init import *
from collections import defaultdict
from pprint import pprint
# --------------------------------parser------------------------------------ #


# start = 'start'
count_for=0
prev_count_for=0

# TODO : Macros, ternary op a>b?1:0 , typedef

''' start symbol of grammar '''
def p_start(p):
    '''
    start : multiple_statements
    '''
    print('printing symbol table....')
    sym_tab.disp()

    print('printing array data stores...')
    com_init.disp()
    print('printing jam table....')
    jam.disp()

    p[0] = p[1]


''' recursion for several statements '''
def p_multiple_statements(p):
    '''
    multiple_statements : multiple_statements statement
                        | statement
    '''

    if(len(p)==3):
        p[0] = [p[1]] + [p[2]]
    else:
        p[0] = p[1]

''' single statement '''
def p_statement(p):
    '''
    statement : open
              | closed
    '''
    p[0] = p[1]

''' open statement '''
def p_open(p):
    '''
    open : IF condition statement
         | IF condition closed ELSE open
         | WHILE condition open
         | for for_condition open
    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
        sym_tab.lookahead(0, len(p[3]), p[3])
    else:
        p[0] = [p[1], [p[2], p[3]], p[4], p[5]]
        sym_tab.lookahead(0, len(p[3]), p[3])
        sym_tab.lookahead(0, len(p[5]), p[5])

''' keyword for '''
def p_for(p):
    '''
    for : FOR
    '''
    global count_for
    global prev_count_for
    prev_count_for = count_for
    count_for+=1
    p[0] = p[1]

''' closed statement '''
def p_closed(p):
    '''
    closed : simple
           | block
           | IF condition closed ELSE closed
           | WHILE condition closed
           | for for_condition closed
    '''
    global count_for
    global prev_count_for
    global loop_var_flags
    if(len(p)==2):
        p[0] = p[1]
    elif(len(p)==4):
        if(p[1] == 'for'):
            print(f"for detected {count_for} {prev_count_for}\n")
            if(True):
                if(count_for==1 and prev_count_for==0):
                    ''' check if comile time initialization is possible '''
                    com_init.compile_init_validate(menu.FLAG_COMPILE_INIT,[p[1], p[2], p[3]])
                    temp = list(set(list(flatten(p[3]))))
                    if(temp.count('{')==1 and temp.count('}')==1 and temp.count(';') and len(temp)==3):
                        p[1] = [None]
                        p[2] = [None]
                        p[3] = [None]
                    nested = False
                else:
                    nested = True

                if(p[1]!=[None] and p[2]!=[None] and p[3]!=[None]):

                    ''' check loop unrolling is possible '''
                    p[0] = for_unroll_validate(menu.FLAG_UNROLL,menu.FLAG_JAMMING,[p[1], p[2], p[3]], nested)

                sym_tab.lookahead(0, len(p[3]), p[3])
                prev_count_for = count_for
                count_for-=1
            else:
                p[0] = [p[1], p[2], p[3]]
        else:
            print("while detected\n")
            p[0] = [p[1], p[2], p[3]]
            sym_tab.lookahead(0, len(p[3]), p[3])
    else:
        p[0] = [p[1],[p[2],p[3]],p[4],p[5]]
        sym_tab.lookahead(0, len(p[3]), p[3])
        sym_tab.lookahead(0, len(p[5]), p[5])



''' conditional '''
def p_condition(p):
    '''
    condition : L_PAREN expr R_PAREN
    '''
    p[0] = [p[1],p[2],p[3]]

''' for loop conditional '''
def p_for_condition(p):
    '''
    for_condition : L_PAREN simple simple expr R_PAREN
                  | L_PAREN simple simple R_PAREN
    '''
    if(len(p) == 6):
        if(p[2]!=';' and p[3]!=';'):
            ids = dict()
            find_id(0,len(p[3]), p[3] , ids)
            loop_var = list(ids.keys())[0]
            do_not_sub = find_lhs_id(0, 1, [p[2]])
            solve_substi_id(0,len(p[2]),p[2], do_not_sub)

        p[0] = [p[1], p[2], p[3], p[4], p[5]]
        if(p[3] != ';'):
            condition = list(map(str, flatten(p[3])))
            loop_var = re.search('([A-Za-z_][A-Za-z_0-9]*)', ''.join(condition)).group(1)
            loop_var_flags[loop_var] = True
            ''' determining nesting '''
            init = flatten(p[2])
            for i in init:
                if i in loop_var_flags and i != loop_var:
                    loop_var_flags[i] = False

            init2 = flatten(p[3])
            for i in init2:
                if i in loop_var_flags and i != loop_var:
                    loop_var_flags[i] = False

            init3 = flatten(p[4])
            for i in init3:
                if i in loop_var_flags and i != loop_var:
                    loop_var_flags[i] = False
    else:
        p[0] = [p[1], p[2], p[3], p[4]]

''' recursion for multiple declarations '''
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
        p[0] = [p[1]] + [p[2], p[3], p[4]]

    elif(len(p)==6):
        if(p[1] == '*'):
            p[0] = [p[1],p[2],p[3],p[4],p[5]]
        else:
            p[0]=p[1]+[p[2],p[3],p[4],p[5]]
    elif(len(p)==7):
        p[0]=p[1]+[p[2],p[3],p[4],p[5],p[6]]
    else:
        p[0]=[p[1],p[2],p[3],p[4]]

''' recursion base '''
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

''' recursion for multiple expressions '''
def p_multi_expr(p):
    '''
    multi_expr : multi_expr expr COMMA
               | expr COMMA
    '''
    if(len(p)==4):
        p[0] = p[1] + [p[2], p[3]]
    else:
        p[0] = [p[1], p[2]]

''' array indexing '''
def p_arrayindex(p):
    '''
    arrayindex : L_SQBRACE index R_SQBRACE
    '''
    p[0] = [p[1],p[2],p[3]]

''' recursion for multidimensional indexing '''
def p_narrayindex(p):
    '''
    narrayindex : narrayindex arrayindex
	    	 | arrayindex
    '''
    if(len(p)==3):
        p[0] = p[1]+p[2]
    else:
        p[0] = p[1]

''' variable declarations '''
def p_declaration(p):
    '''
    declaration : TYPE ID SEMICOLON
                | TYPE ID ASSIGN expr SEMICOLON
                | TYPE MULTIPLY ID ASSIGN expr SEMICOLON
		        | TYPE multi_declaration stop
    			| TYPE ID narrayindex SEMICOLON
    			| TYPE ID narrayindex ASSIGN init_list SEMICOLON
		        | TYPE L_FLOWBRACE multiple_statements R_FLOWBRACE SEMICOLON
		        | TYPEDEF TYPE L_FLOWBRACE multiple_statements R_FLOWBRACE ID SEMICOLON
		        | TYPEDEF TYPE ID SEMICOLON
    '''

    ''' updating symbol table '''
    if(p[2] == "*"):
        search_string = '*' + p[3] + '_'.join(sym_tab.level_str)
        if(p[4] == '='):
            if(type(p[5]) == str):
                dynamic_string = '*' + p[5] + '_'.join(sym_tab.level_str)
                sym_tab.copy_level_str = sym_tab.level_str.copy()
                while(sym_tab.symbol_table[dynamic_string] == 'garbage' and len(sym_tab.copy_level_str)>1):
                    sym_tab.copy_level_str.pop()
                    dynamic_string = '*' + p[5] + '_'.join(sym_tab.copy_level_str)
                if(sym_tab.symbol_table[dynamic_string]!= 'garbage' and sym_tab.symbol_table[dynamic_string]!= 'declared'):
                    sym_tab.symbol_table[search_string ] = sym_tab.symbol_table[dynamic_string]
                else:
                    sym_tab.symbol_table[search_string] = p[5]
            else:
                temp = []
                solve(0, len(p[5]), p[5], temp)
                rhs = ''.join(temp).strip('&')
                dynamic_string = rhs + '_'.join(sym_tab.level_str)
                sym_tab.copy_level_str = sym_tab.level_str.copy()
                while(sym_tab.symbol_table[dynamic_string] == 'garbage' and len(sym_tab.copy_level_str)>1):
                    sym_tab.copy_level_str.pop()
                    dynamic_string = rhs + '_'.join(sym_tab.copy_level_str)
                if(sym_tab.symbol_table[dynamic_string]!='garbage' and sym_tab.symbol_table[dynamic_string]!='declared'):
                    if(re.search(r'(?:\d+\.\d+)|(?:\d+)|(?:".*?")|(?:\'.\')',str(sym_tab.symbol_table[dynamic_string]))):
                        sym_tab.symbol_table[search_string] = rhs
                    else:
                        sym_tab.symbol_table[search_string] = sym_tab.symbol_table[dynamic_string]
                else:
                    sym_tab.symbol_table[search_string] =  rhs

        elif(p[4] == ';'):
            sym_tab.symbol_table[search_string] = 'declared'

        if(sym_tab.symbol_table[search_string]!='garbage' and sym_tab.symbol_table[search_string]!='declared'):
            for var in sym_tab.symbol_table:
                if(
                sym_tab.symbol_table[var]==p[3]):
                    sym_tab.symbol_table[var] = sym_tab.symbol_table[search_string]

    elif(type(p[2])==str):
        if(p[3]== '='):
            search_string = p[2] + '_'.join(sym_tab.level_str)
            if(type(p[4])==int):
                sym_tab.symbol_table[search_string] = p[4]
            elif(type(p[4])==str and re.search(r'[A-Za-z_][A-Za-z_0-9]*',p[4])):
                dynamic_string = p[4] + '_'.join(sym_tab.level_str)
                sym_tab.copy_level_str = sym_tab.level_str.copy()
                while(sym_tab.symbol_table[dynamic_string] == 'garbage' and len(sym_tab.copy_level_str)>1):
                    sym_tab.copy_level_str.pop()
                    dynamic_string = p[4] + '_'.join(sym_tab.copy_level_str)
                if(sym_tab.symbol_table[dynamic_string]!='garbage' and sym_tab.symbol_table[dynamic_string]!='declared'):
                    sym_tab.symbol_table[search_string] = sym_tab.symbol_table[dynamic_string]
                else:
                    sym_tab.symbol_table[search_string] = p[4]
            else:
                sym_tab.symbol_table[search_string] = p[4]

            if(sym_tab.symbol_table[search_string]!='garbage' and sym_tab.symbol_table[search_string]!='declared'):
                for var in sym_tab.symbol_table:
                    if(sym_tab.symbol_table[var]==p[2]):
                        sym_tab.symbol_table[var] = sym_tab.symbol_table[search_string]



        elif( p[3] == ';'):
            sym_tab.symbol_table[p[2] + '_'.join(sym_tab.level_str)] = 'declared'

    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    if(len(p)==5):
        p[0] = [p[1], p[2], p[3], p[4]]
        if(type(p[3])==list and p[3][0]=='['):
            com_init.add_array(menu.FLAG_COMPILE_INIT,p[0])
    if(len(p)==6):
        ''' deals with fn calls in declaration '''
        if(type(p[4]) is list and type(p[4][0]) is tuple and (menu.FLAG_INLINE or menu.FLAG_TAIL_RECURSION)):
            t = p[4][0]
            p[0] = [p[1],p[2],p[3],t[0],'(',t[1][2],')',p[5]]
            call_helper(p[0],t[0])
            p[0] = [(t[0], p[0][3:], "call", p[1], p[2])]
        else:
            p[0] = [p[1], p[2], p[3], p[4], p[5]]

    if(len(p)==7):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
    if(len(p)==9):
        p[0] = [p[1], p[2], p[3], p[4], p[5], p[6] , p[7] , p[8]]


''' array initialization '''
def p_init(p):
    '''
    init : expr COMMA init
    	      | expr
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    if(len(p)==2):
        p[0] = p[1]

''' array init list '''
def p_init_list(p):
    '''
    init_list : L_FLOWBRACE init_list R_FLOWBRACE COMMA init_list
    	      | L_FLOWBRACE init R_FLOWBRACE COMMA init_list
	          | L_FLOWBRACE init R_FLOWBRACE
	          | L_FLOWBRACE init_list R_FLOWBRACE
    '''
    if(len(p)==6):
        p[0] = [p[1],p[2],p[3],p[4],p[5]]
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]

def p_index(p):
    '''
    index : expr
    	  | empty
    '''
    if(p[1]!=None):
        p[0] = p[1]

''' code block '''
def p_block(p):
    '''
    block : left_flower multiple_statements right_flower
          | left_flower right_flower
    '''
    if(len(p) == 4):
        p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = [p[1], p[2]]

''' left flower bracket '''
def p_left_flower(p):
    '''
    left_flower : L_FLOWBRACE
    '''
    sym_tab.level = '%'
    sym_tab.level_str.append(sym_tab.level)
    p[0] = p[1]

''' right flower bracket '''
def p_right_flower(p):
    '''
    right_flower : R_FLOWBRACE
    '''
    sym_tab.level_str.pop()
    p[0] = p[1]



''' statement without constructs '''
def p_simple(p):
    '''
    simple : expr SEMICOLON
           | multi_expr expr SEMICOLON
	       | header
           | declaration
           | SEMICOLON
	       | function
	       | RETURN expr SEMICOLON
           | RETURN SEMICOLON
	       | MULTILINE_COMMENT
    '''
    if(len(p)==3):
        p[0] = [p[1],p[2]]
    elif(len(p)==4):
        if(type(p[2]) is list and type(p[2][0]) is tuple and (menu.FLAG_INLINE or menu.FLAG_TAIL_RECURSION)):
            t = p[2][0]
            p[0] = [p[1], t[0], '(',t[1][2], ')',';']
            call_helper(p[0], t[0])
            p[0] = [(t[0] , p[0][1:] , "call" , "ret" , "ret" ,"return")]
        else:
            p[0] = [p[1], p[2], p[3]]
    else:
        p[0] = p[1]

''' header files are parsed and not preprocessed since they need to be reproduced in the o/p source code '''
def p_header(p):
    '''
    header : HASH INCLUDE STRING
	       | HASH INCLUDE HEADER_FILE
    '''
    p[0] = [p[1],p[2],p[3]+'\n']

def p_empty(p):
    'empty :'
    p[0] = []

''' function call expression '''
def p_function_call(p):
    '''
    function_call : ID L_PAREN call_params R_PAREN
    '''
    p[0] = [p[1], p[2], p[3], p[4]]
    if(menu.FLAG_INLINE or menu.FLAG_TAIL_RECURSION):
        call_helper(p[0],p[1])
        p[0] = [(p[1],p[0][0 : -1], 'call')]

''' function call parameters '''
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

'''  recursion for call parameters '''
def p_yes_call_params(p):
    '''
    yes_call_params : yes_call_params expr COMMA
		            | yes_call_params TYPE COMMA
		            | expr COMMA
			        | TYPE COMMA
    '''
    if(len(p)==3):
        p[0] = [p[1],p[2]]
    else:
        p[0] = p[1] + [p[2],p[3]]

''' recursion base for call parameters '''
def p_end_call_params(p):
    '''
    end_call_params : expr
		            | TYPE
    '''
    p[0] = p[1]


''' recursion for declaration parameters '''
def p_yes_dec_params(p):
    '''
    yes_dec_params : yes_dec_params TYPE expr COMMA
    		       | yes_dec_params TYPE COMMA
                   | yes_dec_params TYPE MULTIPLY COMMA
                   | TYPE expr COMMA
   		           | TYPE COMMA
        	       | TYPE MULTIPLY COMMA
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

''' recursion base for declaration parameters '''
def p_end_dec_params(p):
    '''
    end_dec_params : TYPE expr
		           | TYPE
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

''' declaration parameters '''
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

''' functions '''
def p_function(p):
    '''
    function : TYPE ID L_PAREN dec_params R_PAREN function_2
    '''
    p[0] = [p[1],p[2],p[3],p[4],p[5],p[6]]
    if p[2] != 'main':
        if(p[6][0] != ';' and (menu.FLAG_INLINE or menu.FLAG_TAIL_RECURSION)):
            temp = inline_defn_helper(p[0],p[2])
            p[0] = [temp]

def p_function_2(p):
    '''
    function_2 : SEMICOLON
    	       | block
    '''
    p[0]=[p[1]]


''' below all expr functions are expression parsing '''
def p_expr(p):
    '''
    expr : expr assignment exprOR
         | exprOR
    '''
    if(len(p) > 2 and type(p[1])==str):
        search_string = sym_tab.make_level_string(p[1])
        if(type(p[3])==str and re.search(r'[A-Za-z_][A-Za-z_0-9]*',p[3])):
            if(sym_tab.symbol_table['*' + search_string ] == "garbage" ):
                dynamic_string = sym_tab.make_level_string(p[3])
                if(sym_tab.symbol_table[dynamic_string]!='garbage' and sym_tab.symbol_table[dynamic_string]!='declared'):
                    sym_tab.symbol_table[search_string] = sym_tab.symbol_table[dynamic_string]
                else:
                    sym_tab.symbol_table[search_string] = p[3]
            else:
                dynamic_string = sym_tab.make_level_string("*" + p[3])
                if(sym_tab.symbol_table[dynamic_string]!='garbage' and sym_tab.symbol_table[dynamic_string]!='declared'):
                    sym_tab.symbol_table['*' + search_string ] = sym_tab.symbol_table[dynamic_string]
                else:
                    sym_tab.symbol_table['*' + search_string] = p[3]

        elif(sym_tab.symbol_table['*' + search_string ] != "garbage" and type(p[3])==list):
            temp = []
            solve(0, len(p[3]), p[3], temp)
            rhs = ''.join(temp).strip('&')
            dynamic_string = sym_tab.make_level_string(rhs)

            if(sym_tab.symbol_table[dynamic_string]!='garbage' and sym_tab.symbol_table[dynamic_string]!='declared'):
                    if(re.search(r'(?:\d+\.\d+)|(?:\d+)|(?:".*?")|(?:\'.\')',str(sym_tab.symbol_table[dynamic_string]))):
                        sym_tab.symbol_table['*'+search_string] = rhs
                    else:
                        sym_tab.symbol_table['*'+search_string] = sym_tab.symbol_table[dynamic_string]
            else:
                sym_tab.symbol_table['*'+search_string] =  rhs
        else:
            sym_tab.symbol_table[search_string] = p[3]

        if(sym_tab.symbol_table[search_string]!='garbage' and sym_tab.symbol_table[search_string]!='declared'):
            for var in sym_tab.symbol_table:
                if(sym_tab.symbol_table[var]==p[1]):
                    sym_tab.symbol_table[var] = sym_tab.symbol_table[search_string]

        if(sym_tab.symbol_table['*'+search_string]!='garbage' and sym_tab.symbol_table['*'+search_string]!='declared'):
            for var in sym_tab.symbol_table:
                if(sym_tab.symbol_table[var]==p[1]):
                    sym_tab.symbol_table[var] = sym_tab.symbol_table['*'+search_string]

    if(len(p)==4):
        if(type(p[3]) is list and type(p[3][0]) is tuple):
            t = p[3][0]
            p[0] = [p[1],p[2],t[0],'(',t[1][2],')']
            if(menu.FLAG_INLINE or menu.FLAG_TAIL_RECURSION):
                call_helper(p[0],t[0])
                p[0] = [ ( t[0] , p[0][2:] , "call" , p[1])]
        else:
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

''' still expressions '''
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

''' still expressions '''
def p_factor(p):
    '''
    factor : NOT factor
           | PLUS factor
           | MINUS factor
           | PLUS_PLUS factor
           | MINUS_MINUS factor
           | cast brace
	       | brace
    '''
    if(len(p)==3):
        if(p[1]=='++' or p[1]=='--'):
            if(type(p[2])==str):
                sym_tab.symbol_table[sym_tab.make_level_string(p[2])] = 'declared'
                p[0] = [p[1], p[2]]
            else:
                var_dict = {}
                find_id(0,len(p[2]),p[2],var_dict)
                var =list(var_dict.keys())[0]
                sym_tab.symbol_table[sym_tab.make_level_string(sym_tab.symbol_table[sym_tab.make_level_string('*'+var)])] = 'declared'
                p[0] = [p[1], p[2]]
        elif(p[1] == '-' and type(p[2])!=list and type(p[2])!=str):
            p[0] = -1*p[2]
        else:
            p[0] = [p[1],p[2]]
    else :
        p[0] = p[1]

''' type casting '''
def p_cast(p):
    '''
    cast : L_PAREN TYPE R_PAREN
	     | L_PAREN TYPE MULTIPLY R_PAREN
    '''
    if(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
    elif(len(p)==5):
        p[0] = [p[1],p[2],p[3],p[4]]

''' expression base '''
def p_brace(p):
    '''
    brace  : L_PAREN expr R_PAREN
           | brace PLUS_PLUS
           | brace MINUS_MINUS
           | NUM
           | STRING
           | MULTIPLY ID
           | BIT_AND ID
	       | BIT_AND ID narrayindex
           | ID
    	   | CHAR
           | function_call
    	   | ID narrayindex
	       | arrow
	       | dot

    '''
    if(len(p)==4):
        p[0] = [p[1], p[2], p[3]]
    elif(len(p)==5):
        p[0] = [p[1], p[2], p[3],p[4]]
    elif(len(p)==3):
        if(p[2]=='++' or p[2] =='--'):
            if(type(p[1])==str):
                sym_tab.symbol_table[sym_tab.make_level_string(p[1])] = 'declared'
            else:
                if(p[1][0]=='*'):
                    sym_tab.symbol_table[sym_tab.make_level_string('*'+p[1][-1])] = 'declared'
                else:
                    var_dict = {}
                    find_id(0,len(p[1]),p[1],var_dict)
                    var =list(var_dict.keys())[0]
                    sym_tab.symbol_table[sym_tab.make_level_string(sym_tab.symbol_table[sym_tab.make_level_string('*'+var)])] = 'declared'
        p[0] = [p[1], p[2]]
    else:
        if(type(p[1]) is list and type(p[1][0]) is tuple):
            t = copy.deepcopy(p[1][0])
            t = list(flatten(t))
            print('\n\np[1] (1) in p_brace : ', p[1], '\n\n')
            if(t.count("call") > 1):
                print('\n\np[1] (2) in p_brace : ', p[1], '\n\n')
                remove_nested_calls(0,len(p[1]),p[1])
                print('\n\np[1] (3) in p_brace : ', p[1], '\n\n')
            del(t)
        p[0] = p[1]

''' arrow dereference '''
def p_arrow(p):
    '''
    arrow : ID ARROW ID
    '''
    p[0] = [p[1],p[2],p[3]]

''' dot dereference '''
def p_dot(p):
    '''
    dot : ID DOT ID
    '''
    p[0] = [p[1],p[2],p[3]]

''' number literals '''
def p_NUM(p):
    '''
    NUM : INT_NUM
	    | FLOAT_NUM
    '''
    p[0] = p[1]

def p_error(p):
    print(f"an error occurred ::: token {p} , char {p.value}")

''' flattening function to flatten nested loops '''
def flatten(L):
    for l in L:
        if isinstance(l, list):
            yield from flatten(l)
        else:
            yield l
