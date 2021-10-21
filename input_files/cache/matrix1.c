#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int n = 256;
double c[256][256];
 void init(double a[][n])
 {
 	for(int i = 0; i < n; ++i)
 	{
 		for(int j = 0; j < n; ++j)
 		{
 			a[i][j] = rand();
 		}
 	}

 }
void multiply(double a[][n], double b[][n], double c[][n])
{
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      for (int k = 0; k < n; ++k) {
        c[i][j] += a[i][k] * b[k][j];
      }
    }
  }
}


int main()
{
  double a[n][n];
  double b[n][n];
  init(a);
  init(b);
  multiply(a, b, c);
  printf("the end\n");
}
