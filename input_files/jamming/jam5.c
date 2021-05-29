#include<stdio.h>
int main()
{
  int n;
  int a = 0;
  int b = 0;
  scanf("%d", &n);
  for(int i = 1; i < n; ++i)
  {
    ++a;
  }
  for(int i = 1; i < n + 1; ++i)
  {
    ++b;
  }
  printf("a : %d, b : %d", a, b);
}
