//find min of x, y
#include<stdio.h>

int main()
{
    int x=1, y=2;
    int r;
    if(x>y) {
        r = y;
    }
    else {
        r = x;
    }
    printf("Min of %d, %d is: %d\n", x, y, r);
    if(x>=y) {
        r = y;
    }
    else {
        r = x;
    }
    printf("Min of %d, %d is: %d\n", x, y, r);
    return 0;
}