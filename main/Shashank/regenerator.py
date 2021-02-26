
#----------------------------------------------code generator ------------------------------------------------------

def solve(i,n,l,output_prg):
    if(i==n):
        return
    elif(type(l[i]) is str):
        if(l[i] == 'int' or l[i] == 'float' or l[i] == 'return'):
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

#-----------------------------------------------------------------------------------------------------------------------
