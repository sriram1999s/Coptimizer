//find min of x, y
#include<stdio.h>

int main()
{
    int x=1;
    int y=2;
    int r;
    if(x<y) {
        r = x;
    }
    else {
        r = y;
    }
    printf("Min of %d, %d is: %d\n", x, y, r);

    if(x<=y) {
        r = x;
    }
    else {
        r = y;
    }
    printf("Min of %d, %d is: %d\n", x, y, r);

    if(10<=20) {
        r = 10;
    }
    else {
        r = 20;
    }
    printf("Min of 10, 20 is: %d", r);
    return 0;
}