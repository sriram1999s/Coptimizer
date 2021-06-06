#include<stdio.h>

int main() {
  int n;
  scanf("%d",&n);         
  int a=0;
  int b=0;
  int k=3;
  for(int j=k;j<n;j+=1) {             
      a++;
    }
  for(int j=n-1;j>k+1;j-=1) {             
      b++;
    }

  printf("%d %d\n",a,b);
}
  


