#include<stdio.h>
int main()
{
  int n;
  int a = 0;
  int b = 0;
  scanf("%d", &n);
  for(int i = 0; i < n; ++i)
  {
    ++a;
  }
  for(int i = 2; i < n; ++i)
  {
    ++b;
  }
  printf("a : %d, b : %d", a, b);
}
