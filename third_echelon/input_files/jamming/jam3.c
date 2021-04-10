#include<stdio.h>
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
  for(int i = 0; i < n; ++i)
  {
    ++*p;
  }
}
