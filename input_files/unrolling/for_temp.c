#include<stdio.h>
int main()
{
  int a =5 ;
  int k = 0;
  int *q;
  int *p=q;
  q=&a;
  for(int i = 0;i < a; ++i)
  {
    (*p)++;
    ++k;
  }
}
