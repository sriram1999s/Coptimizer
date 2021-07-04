#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;
	int choice = 1;
	switch (choice) {
	case 0:{
			int option = 10;
			if (option <= 10) {
				if (option < 10) {
					int temp;
				} else if (option == 10) {
					int temp1;
				} else if (option == 90) {
					int temp2;
				}
			} else if (option == 20) {
				int temp3;
			}
		} break;
	case 1:{
			int temp4;
		} break;
	default:{
			int temp5;
		} break;
	}
	double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile.txt","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);return 0;
}
