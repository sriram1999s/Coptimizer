#include <stdio.h>

/* predicate-begin */
int predicate(int x)
{
  // return (2*x>9) || ((x<7) && (x>1));
  // return (2*x>3) && (x<7);
  return (((x<-3) || (x>3)) && (x>4)) || (x<-2);
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
