#include<stdio.h>
int main() {
    int c[20];
    int a[] = {1,2,3,4};
    int b[50];
    int j=2;
    for(int i = 0;i<10;i++)
    {
	     b[2*i] = i*i*i;
       c[i] = i*i;
	     j=j+1;
    }
}
