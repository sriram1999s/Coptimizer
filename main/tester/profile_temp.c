#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
void print(int n)
{
 label_68362a3c20c2483c902950f253ee08fa:{
	}
	if (n < 0) {
		return;
	}
	printf(" %d", n); {	// tail recursion eliminated
		int par_n_68362a3c20c2483c902950f253ee08fa = n;
		n = par_n_68362a3c20c2483c902950f253ee08fa - 1;
		goto label_68362a3c20c2483c902950f253ee08fa;
	};
}

int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;
	print(100000);
	printf("\n");
	double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);return 0;
}
