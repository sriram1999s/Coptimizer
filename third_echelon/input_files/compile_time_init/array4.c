#include<stdio.h>
int main() {
    int c[20];
    int a[] = {1,2,3,4};
    int k=0;
    int j=2;
    for(int i = k;i< 5;++i)
    {
	int b[20];
	for(int j=0;j<5;j++) {
	    b[j] = 0;
	}
        c[i] = 1;
	j=j+1;
    }
}
