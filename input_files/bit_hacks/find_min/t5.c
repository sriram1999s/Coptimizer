//find min of x, y
#include<stdio.h>

int main()
{
    char x='a', y='b';
    char r;
    if(x<y) {
        r = x;
    }
    else {
        r = y;
    }
    printf("Min of %c, %c is: %c\n", x, y, r);
    return 0;
}