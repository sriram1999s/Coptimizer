#include<stdio.h>
int main() {
    int a=0;
    int n;
    scanf("%d",&n);
    for(int i=n;i>-1;i-=5) {
	a++;
    }
    printf("\na: %d\n",a);
}
