import re
import sys

try:
    f = sys.argv[1]
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

final_string = '#include<time.h>\n#include<string.h>\n' + source[0:ind] + '{' + 'double startTime = (float)clock()/CLOCKS_PER_SEC;' + captured_string[0:-1] + 'double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; FILE *fp = fopen("profile","w"); fprintf(fp,"%f\\n",timeElapsed); fclose(fp);' + '}' + source[end_ind:]

print(final_string)

        
    

 

