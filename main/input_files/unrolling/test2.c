#include<stdio.h>

void looping(int n) {
    int a=0;
    for(int i=0;i<n;i++) {
    a++;
}
    printf("%d\n",a);
}

int main() {
    int n1;
    int n2;
    int n3;
    scanf("%d",&n1);
    scanf("%d",&n2);
    scanf("%d",&n3);
    looping(n1);
    looping(n2);
    looping(n3);
}
