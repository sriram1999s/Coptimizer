//find min of x, y
#include<stdio.h>

int main()
{
    float x=1.1, y=2.1;
    float r;
    if(x<y) {
        r = x;
    }
    else {
        r = y;
    }
    printf("Min of %f, %f is: %f\n", x, y, r);
    return 0;
}