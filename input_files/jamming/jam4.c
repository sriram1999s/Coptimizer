#include<stdio.h>

/* Not working */
int main()
{
  int n;
  int a = 0;
  int b = 0;
  int *p = &a;
  scanf("%d", &n);
  for(int i = 0; i < n; ++i)
  {
    ++a;
    ++b;
  }
  int sum = 0;
  for(int i = 0; i < n; ++i)
  {
    sum += a;
  }
}
