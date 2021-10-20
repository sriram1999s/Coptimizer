#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* void init(double a[][n], int n) */
/* { */
/* 	for(int i = 0; i < n; ++i) */
/* 	{ */
/* 		for(int j = 0; j < n; ++j) */
/* 		{ */
/* 			a[i][j] = rand(); */
/* 		} */
/* 	} */

/* } */

void multiply(double a[][n], double b[][n], double c[][n], int l, int m, int n)
{
  for (int i = 0; i < l; ++i) {
    for (int j = 0; j < n; ++j) {
      for (int k = 0; k < m; ++k) {
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
  multiply(a, b, c, n, n, n);
  printf("the end\n");
}
