#include<stdio.h>

int main()
{
    int x = 6, y = 5, n = 10;
    int r = (x+y)%n;
    printf("%d\n", r);

    r = (x)+y%n;
    printf("%d\n", r);

    r = x+(y)%n;
    printf("%d\n", r);

    r = (x)+(y)%n;
    printf("%d\n", r);

    r = (((x+y)))%n;    // needs to be changed to bit hack
    printf("%d\n", r);

    r = ((x)+y)%n;  // needs to be changed to bit hack?
    printf("%d\n", r);

    return 0;
}