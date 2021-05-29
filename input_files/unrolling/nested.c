#include<stdio.h>

int main()
{
  int a = 4;
  int k = 4;
  int n;
  scanf("%d", &n);
  for(int i = 0; i < n; ++i)
  {
    for(int j =  i + a; j < n + 3; ++j)
    {
      ++a;
    }
  }
  for(int i = 0; i < n; ++i)
  {
    for(int j =  k; j < n + 3; ++j)
    {
      ++a;
    }
  }
  printf("%d\n", a);
}
