#include<stdio.h>
int main() {
    int a=10;
    int n;
    int b=7;
    scanf("%d",&n);
    int *p;
    int *q;
    q=&a;
    {
      p=q;
    }
    for(int i=0;i<a;i++) {
    *p++;
    }
    printf("\na: %d\n",a);
}
