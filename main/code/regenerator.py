
# ----------------------------------------------code generator ------------------------------------------------------



def solve(start_index, end_index, parse_tree, output_prg):
    space_list = ['int','float','void','return']
    if(start_index == end_index):
        return
    elif(type(parse_tree[start_index]) is str):
        if(parse_tree[start_index]=='int' or parse_tree[start_index]=='float' or parse_tree[start_index]=='void' or parse_tree[start_index]=='return'):
            print("here",parse_tree[start_index])
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
                if(parse_tree[start_index][trav]=='int' or parse_tree[start_index][trav]=='float' or parse_tree[start_index][trav]=='void' or parse_tree[start_index][trav]=='return'):
                    output_prg += [parse_tree[start_index][trav], ' ']
                else:
                    output_prg += [str(parse_tree[start_index][trav])]
        solve(start_index+1, end_index, parse_tree, output_prg)

# -----------------------------------------------------------------------------------------------------------------------
