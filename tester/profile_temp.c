#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
int check_overlap(int x1, int y1, int x2, int y2)
{
	if (x1 > y1 || x2 > y2)
		return 0;
	if ((x1 >= x2 && x1 < y2) || (y1 > x2 && y1 <= y2)
	    || ((x1 < y1 ? x1 : y1) > (x2 < y2 ? x2 : y2)
		&& (x1 > y1 ? x1 : y1) < (x2 > y2 ? x2 : y2))
	    || ((x1 < y1 ? x1 : y1) < (x2 < y2 ? x2 : y2)
		&& (x1 > y1 ? x1 : y1) > (x2 > y2 ? x2 : y2)))
		return 1;
	return 0;
}

int main()
{struct rusage r_usage;double startTime = (float)clock()/CLOCKS_PER_SEC;
	int n;
	scanf("%d", &n);
	int a = 0;
	int b = 0;
	int k = 3;
	if (check_overlap(4 + 1, n - 1 + 1, 3, n)) {
		int temp_bb0d6b7362c5 = 3;
		int temp_aefff4a407bd = (n - 1 + 1 < n ? n - 1 + 1 : n);
		int temp_258e57444e1a = 5;
		int temp_6576ba88f268 = (n - 1 + 1 > n ? n - 1 + 1 : n);
		for (int j = temp_258e57444e1a; j < temp_aefff4a407bd; j += 1) { {
				a++;
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
		} {
			b++;
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
		}} for (int j = 0; j < (temp_258e57444e1a - temp_bb0d6b7362c5);
			j += 1) {
			if (temp_bb0d6b7362c5 == 3) { {
					a++;
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
			}
			} else { {
					b++;
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
			}
			}
		}
		for (int z = 0; z < (temp_6576ba88f268 - temp_aefff4a407bd);
		     z++) {
			if (temp_6576ba88f268 == n) { {
					a++;
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
			}
			} else { {
					b++;
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
			}
			}
		}
	} else {
		for (int j = n - 1; j > 4; j -= 1) {
			b++;
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
		} for (int j = 3; j < n; j += 1) {
			a++;
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
	}} printf("%d %d\n", a, b);
double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}
