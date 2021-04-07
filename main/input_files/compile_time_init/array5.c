#include<stdio.h>
int main() {
    int c[20];
    int a[] = {1,2,3,4};
    int b[20];
    int j=2;
    for(int i = 0;i< 5;++i)
    {
	b[i] = 0; 
        c[i] = 1;
	j=j+1;
    }
    printf("\n%d\n",b[0]); 
    for(int i = 0;i<10;++i) {
	b[i] = 1;
    }
}
