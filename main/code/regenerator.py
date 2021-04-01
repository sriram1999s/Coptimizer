
# ----------------------------------------------code generator ------------------------------------------------------



def solve(start_index, end_index, parse_tree, output_prg):
    space_list = ['int','float','void','double','bool','char','return']
    if(start_index == end_index):
        return
    elif(type(parse_tree[start_index]) is str):
        if(start_index+1<end_index and parse_tree[start_index] in space_list and parse_tree[start_index+1]!=' '):
            output_prg += [parse_tree[start_index], ' ']
        else:
            output_prg += [parse_tree[start_index]]
        solve(start_index+1, end_index, parse_tree, output_prg)
    elif(type(parse_tree[start_index]) is int):
        output_prg += [str(parse_tree[start_index])]
        solve(start_index+1, end_index, parse_tree, output_prg)

    elif(type(parse_tree[start_index]) is tuple or type(parse_tree[start_index]) is list):
        for trav in range(len(parse_tree[start_index])):
            if(type(parse_tree[start_index][trav]) is tuple or type(parse_tree[start_index][trav]) is list):
                solve(0, len(parse_tree[start_index][trav]), parse_tree[start_index][trav], output_prg)
            else:
                if(trav+1<end_index and parse_tree[start_index][trav] in space_list and parse_tree[start_index][trav+1]!=' '):
                    output_prg += [parse_tree[start_index][trav], ' ']
                else:
                    output_prg += [str(parse_tree[start_index][trav])]
        solve(start_index+1, end_index, parse_tree, output_prg)

# -----------------------------------------------------------------------------------------------------------------------
