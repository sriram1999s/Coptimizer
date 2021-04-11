#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;
	int a = 2;
	switch (a) {
	case 1:{
			int c;
		} break;
	case 2:{
			int d = 100;
			if (d == 100 || d == 200) {
				int e = -1;
				if (e == 0) {
					int printf1;
				} else if (e == 1) {
					int printf2;
					switch (e) {
					case 1:
						if (d == 100) {
							int printf3;
						}
						break;
					case 0:
						if (d == 100) {
							int b = 30;
							switch (b) {
							case 20:{
									int f;
								} break;
							case 30:{
									int g;
								} break;
							}
						}
						break;
					case -1:
						if (d == 100) {
							int b = 30;
							switch (b) {
							case 20:{
									int f;
								} break;
							case 30:{
									int g;
								} break;
							}
						}
						break;
					}
				} else if (d == 100) {
					int h;
				}
			}
		} break;
	default:{
			int i;
		} break;
	}
	return 0;
double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}
