#include <stdio.h>

/* predicate-begin */
int predicate(int a)
{
  if (a & 1) {
    printf("it is odd!\n");
    return 1;
  }
  if (a % 11) {
    printf("divisible by 11\n");
    return 1;
  }
  return 0;
}
/* predicate-end */

int main()
{
  /*data-structure:array*/
  int a[] = {5, 8, 3, 2, 12, 17, 19, 30};
  int n = sizeof(a) / sizeof(int);
  int elem = 2;
  int i = 0;
  /*linear-search-begin*/
  while (i < n) {
    if (predicate(a[i])) {
      break;
    }
    i++;
  }
  /*linear-search-end*/
}
