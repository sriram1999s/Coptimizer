#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;{
	int a = 0;
	int n;
	scanf("%d", &n);
	int temp_4fb9a0c9485a76554cd0abfee6ff2fdc =
	    (((n - (-2)) / 1) + (((n - (-2)) % 1) != 0));
	int temp_loop_cd2f769cb40022fe0cd9621d4a7d5f89;
	for (int i = 0;
	     i <
	     (temp_4fb9a0c9485a76554cd0abfee6ff2fdc -
	      (temp_4fb9a0c9485a76554cd0abfee6ff2fdc % 2)) / 2; i++) { {
			temp_loop_cd2f769cb40022fe0cd9621d4a7d5f89 = i;
	} {
		a++;
	} {
		a++;
	}} if ((temp_4fb9a0c9485a76554cd0abfee6ff2fdc % 2)) { {
			a++;
	}
	}
	printf("\na: %d\n", a);double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}}
