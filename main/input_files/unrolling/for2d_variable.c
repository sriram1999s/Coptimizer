#include<stdio.h>

int looping(int n,int m) {
    int a=0;
    for(int i=0;i<n;i++) {
	for(int j=i;j<m;j++) {
	    a++;
	}
    }
    printf("%d\n",a);
}

int main() {
    looping(3,3);
}
