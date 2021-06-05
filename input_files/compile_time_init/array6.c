#include<stdio.h>
int main() {
    int c[20];
    int a[] = {1,2,3,4};
    int b[20];
    int j=2;
    for(int i = 0;i< 20;i+=1)
    {
	       b[i] = i;
         c[i] = i;
	       j=j+1;
    }
}
