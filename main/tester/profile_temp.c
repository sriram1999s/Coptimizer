#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;
	int i;
	int j;
	int rows;
	int a = 0;
	printf("Enter the number of rows: \n");
	scanf("%d", &rows);
	for (i = 1; i < rows + 1; ++i) {
		int temp_c6aeb7d243687c83ab7735c9d2ec7c9c =
		    (((i + 1 - (1)) / 1) + (((i + 1 - (1)) % 1) != 0));
		int temp_loop_43d19f046c2c5fcf8dc7b8fb910d2358;
		for (int j = 0;
		     j <
		     (temp_c6aeb7d243687c83ab7735c9d2ec7c9c -
		      (temp_c6aeb7d243687c83ab7735c9d2ec7c9c % 2)) / 2; j++) { {
				temp_loop_43d19f046c2c5fcf8dc7b8fb910d2358 = j;
		} {
			printf("* ");
		} {
			printf("* ");
		}} if ((temp_c6aeb7d243687c83ab7735c9d2ec7c9c % 2)) { {
				printf("* ");
		}
		}
		printf("\n");
	}
double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}
