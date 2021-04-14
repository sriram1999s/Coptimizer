import re
import sys

#include<stdio.h>
#include <sys/resource.h>
#include <errno.h>
#include<time.h>



def profile(file):
    try:
        f = file
    except:
        print("file error")


    source = ''
    with open(f) as fi:
        for line in fi:
            source += line

    m = re.search(r'\bmain\s*\(.*?\)\s*{',source,re.S)
    ind = (m.span()[-1])-1
    captured_string = ""
    end_ind = 'x'
    level=0
    for i in range(ind,len(source)):
        if(source[i]=='}'):
            level-=1
        elif(source[i]=='{'):
            level+=1
        if(level==0):
            end_ind = i
            break
        captured_string+=source[i]

   

    headers = '#include<time.h>\n#include<string.h>\n#include<sys/resource.h>\n#include <errno.h>\n#include<stdio.h>\n'

    print("captured_string: ",captured_string)

    return_match = re.search(r'return\s+?0\s*?;',captured_string)
    if(return_match):
        end_ind_ret=return_match.span()[0]
        final_string =  headers + source[0:ind] + '{' +'struct rusage r_usage;' + 'double startTime = (float)clock()/CLOCKS_PER_SEC;' + captured_string[1:end_ind_ret] + 'double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");\nif(ret == 0)\nfprintf(fp,"%ld\\n",r_usage.ru_maxrss);\nelse\nfprintf(fp,"%d\\n", -1);' + 'fprintf(fp,"%f\\n",timeElapsed); fclose(fp);' + 'return 0;\n}' + source[end_ind+1:]
    else:
        final_string =  headers + source[0:ind] + '{' +'struct rusage r_usage;' + 'double startTime = (float)clock()/CLOCKS_PER_SEC;' + captured_string[1:] + 'double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");\nif(ret == 0)\nfprintf(fp,"%ld\\n",r_usage.ru_maxrss);\nelse\nfprintf(fp,"%d\\n", -1);' + 'fprintf(fp,"%f\\n",timeElapsed); fclose(fp);' + '}' + source[end_ind+1:]

    return final_string

        
    

 

