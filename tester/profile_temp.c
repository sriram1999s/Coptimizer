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
	scanf("%d", &n);	/* n = 4 */
	int a = 0;
	int b = 0;
	int c = 0;
	for (int i = 0; i < n; i++) {	/* [0,4) */
		if (check_overlap(i + 1, n, i + 2 + 1, n - 1 + 1)) {
			int temp_3bc9cf357b18 =
			    (i + 1 < i + 2 + 1 ? i + 1 : i + 2 + 1);
			int temp_a1606e38b9a4 = (n < n - 1 + 1 ? n : n - 1 + 1);
			int temp_7253e101df7a =
			    (i + 1 > i + 2 + 1 ? i + 1 : i + 2 + 1);
			int temp_61be0f576948 = (n > n - 1 + 1 ? n : n - 1 + 1);
			for (int j = temp_7253e101df7a; j < temp_a1606e38b9a4; j += 1) { {	/* [i+1,4) */
					a++;
			} {	/* [i+2,n-1)    i+3-n */
				b++;
			}} for (int j = 0;
				j < (temp_7253e101df7a - temp_3bc9cf357b18);
				j += 1) {
				if (temp_3bc9cf357b18 == i + 2 + 1) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
			for (int z = 0;
			     z < (temp_61be0f576948 - temp_a1606e38b9a4); z++) {
				if (temp_61be0f576948 == n - 1 + 1) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
		} else {
			for (int j = i + 1; j < n; j += 1) {	/* [i+2,n-1)    i+3-n */
				b++;
			} for (int j = i + 2 + 1; j < n - 1 + 1; j += 1) {	/* [i+1,4) */
				a++;
	}}} for (int i = 1; i < n - 1; i++) {
		c++;
	} printf("%d %d %d\n", a, b, c);
double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}
