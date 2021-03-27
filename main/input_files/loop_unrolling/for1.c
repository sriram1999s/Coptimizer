#include<stdio.h>
int main()
{
  int a;
  int z = 1;
  int n;
  scanf("%d %d",&a,&n);
  for(int i = a;i>n;i=i/2)
  {
    ++z;
  }
  printf("\n res: %d\n",z);
}
