#include<stdio.h>

void looping(int n) {
    int a=0;
    for(int i=0;i<n;i++) {
	a++;
}
    printf("%d\n",a);
}

int main() {
    looping(1000000000);
    looping(1000000000);
    looping(100000000);
}
