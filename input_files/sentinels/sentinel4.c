#include <stdio.h>

/* predicate-begin */
int predicate(int a)
{
  return (a - 1) == 7;
}
/* predicate-end */

int main()
{
  /*data-structure:array*/
  int a[] = {5, 8, 3, 2, 12, 17, 19, 32};
  int n = sizeof(a) / sizeof(int);
  int elem = 2;
  int i = 0;
  /*linear-search-begin*/
  while (i < n) {
    if (predicate(a[i])) {
      printf("Predicate True\n");
      break;
    }
    i++;
  }
  /*linear-search-end*/
}
