#include <stdio.h>

int main()
{
  /*data-structure:array*/
  int a[] = {5, 8, 3, 2, 12, 17, 19, 30};
  int n = sizeof(a) / sizeof(int);
  int elem = 19;
  int i = 0;
  /*linear-search-begin*/
  while (i < n) {
    if (a[i] == elem) {
      printf("%d.....found", elem);
      break;
    }
    i++;
  }
  /*linear-search-end*/
}
