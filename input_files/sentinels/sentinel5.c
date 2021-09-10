#include <stdio.h>

int main()
{
  /*data-structure:array*/
  int a[] = {5, 8, 3, 2, 12, 17, 19, 33};
  int n = sizeof(a) / sizeof(int);
  int elem = 2;
  int i = 0;
  /*linear-search-begin*/
  while (i < n) {
    if (a[i] % 2 == 0) {
      printf("Predicate True\n");
      break;
    }
    i++;
  }
  /*linear-search-end*/
}
