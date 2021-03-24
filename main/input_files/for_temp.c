#include<stdio.h>
int main()
{
  int a =5 ;
  int k = 0;
  int *q;
  int *p=q;
  q=&a;
  if(k)
  {
    ++*p;
  }
  for(int i = 0;i < *p; ++i)
  {
    ++k;
  }
}
