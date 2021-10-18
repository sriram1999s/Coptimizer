#include <stdio.h>
#include <time.h>
int main()
{
  int a = 0;
  int n;
  scanf("%d", &n);
  int c_i = 0;
  for (int i = 0; i < n; i++) {
    a = a + c_i;
    ++c_i;
  }
  printf("%d\n", a);
}
