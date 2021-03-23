#include<stdio.h>
int main()
{
  int a =5 ;
  int k = 0;
  int *p = &a;
  for(int i = 0;i < 10; ++i)
  {
    *p++;
  }
  for(int i = 0;i < a; ++i)
  {
    ++k;
  }
}
