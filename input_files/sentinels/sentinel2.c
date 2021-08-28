#include <stdio.h>

int main()
{
  /*data-structure:array*/
  int a[] = {5, -8, 10, 2};
  int n = sizeof(a) / sizeof(int);
  int sum1 = 0;
  int i = 0;
  /*overflow-begin*/
  while (i<n) {
//    sum1 = sum1 + a[i];
    if (sum1<a[i]) {
      printf("%d.....overflow", sum1);
      break;
    }
    sum1 = sum1 + a[i];
    ++i;
  }
  /*overflow-end*/
}


