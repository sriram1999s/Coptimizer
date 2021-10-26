//find min of x, y
#include<stdio.h>

int main()
{
    int x=1, y=2;
    int r=0;
    if(x<y) {
        r = r+x;
    }
    else {
        r = r+y;
    }
    printf("Min of %d, %d is: %d\n", x, y, r);
    return 0;
}