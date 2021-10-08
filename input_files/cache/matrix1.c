#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

double time_elapsed(struct timespec start, struct timespec end)
{
	double t;
	t = (end.tv_sec - start.tv_sec);
	t += (end.tv_nsec - start.tv_nsec) * 0.000000001;
	return t;
}

void init(int n; double a[][n], int n)
{
	for(int i = 0; i < n; ++i)
	{
		for(int j = 0; j < n; ++j)
		{
			a[i][j] = rand();
		}
	}

}
// A[l, m], B[m, n], C[l, n]
void multiply(int n; double a[][n], double b[][n], double c[][n], int l, int m, int n)
{
	for(int i = 0; i < l; ++i)
	{
		for(int j = 0; j < n; ++j)
		{
			c[i][j] = 0.0;
			for(int k = 0; k < m; ++k)
			{
				c[i][j] += a[i][k] * b[k][j];
			}

		}
	}
}

int main()
{
	int n = 256;
	double a[n][n];
	double b[n][n];
	double c[n][n];
	init(a, n);
	init(b, n);
	struct timespec start;
	struct timespec end;
	clock_gettime(CLOCK_REALTIME, &start);
	multiply(a, b, c, n, n, n);
	clock_gettime(CLOCK_REALTIME, &end);
	printf("time %lf \n",
			   time_elapsed(start, end));
	printf("the end\n");

}
