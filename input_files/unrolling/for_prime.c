#include<stdio.h>

int main() {
    int n;
    scanf("%d",&n);
    int c=0;
    int c_i = 1;
    for(int i=1;i<n+1;i++) {
	c+=c_i;
	c_i++;
    }
    printf("%d\n",c);
}
