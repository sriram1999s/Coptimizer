#include<stdio.h>
int main()
{
  int a;
  int z = 1;
  int n;
  scanf("%d %d",&a,&n);
  int i, u;
  for(i = a, u = 0; i > n; i = i / 2)
  {
    ++z;
  }
  printf("\n res: %d\n",z);
}
