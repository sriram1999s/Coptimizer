#include<stdio.h>

void fact(int n, double a){
   if(n == 0) {
      printf("factorial : %f\n", a);
   } else { fact(n-1, a*n);
}
}

int main()
{
  fact(10,1);
  return 0;
}
