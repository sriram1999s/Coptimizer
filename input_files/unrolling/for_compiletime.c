#include <stdio.h>

/* predicate-begin */
int predicate(int x)
{
  return ((x > 56) && (x < 89));
}
/* predicate-end */

int main()
{
  /*data-structure:array */
  int a[50];

  /* initializing array */
  for (int i = 0; i <= 49; i++) {
    a[i] = 2 * i - 1;
  }

  int i = 0;
  int n = 50;

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
