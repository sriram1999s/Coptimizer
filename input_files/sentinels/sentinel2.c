#include <stdio.h>

int main()
{
  /*data-structure:array*/
  int a[] = {5, 8, 3, 2, 12, 17, 19, 30};
  int n = sizeof(a) / sizeof(int);
  int elem = 2;
  int i = 0;
  /*linear-search-begin*/
  while (i < n) {
    if (a[i] == elem) {
      printf("%d.....found", elem);
      break;
    }
    if (a[i] & 1) {
      printf("%d....is odd", elem);
      break;
    }
    if (a[i] % 11 == 0) {
      printf("%d...divisible by 11", elem);
      break;
    }
    i++;
  }
  /*linear-search-end*/
}
