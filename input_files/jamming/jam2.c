#include <stdio.h>
int main()
{
  int n;
  int a = 0;
  int b = 0;
  int k = 0;
  scanf("%d", &n);
  for (int i = 0; i < n; ++i) {
    ++a;
  }
  for (int i = 0; i < n + 1; ++i) {
    ++b;
  }
  for (int i = 0; i < n; ++i) {
    k = k + 1;
  }
}
