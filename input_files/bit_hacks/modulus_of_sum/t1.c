#include<stdio.h>

int main()
{
    int x = 6;
    int y = 5;
    int n = 10;
    int r = (x+y)%n;
    printf("%d\n", r);

    r = (x+y)%(n);
    printf("%d\n", r);

    r = (x)+y%n;
    printf("%d\n", r);

    r = x+(y)%n;
    printf("%d\n", r);

    r = (x)+(y)%n;
    printf("%d\n", r);

    r = (((x+y)))%n;
    printf("%d\n", r);

    r = ((x)+y)%n;  // won't be changed to bit hack
    printf("%d\n", r);

    return 0;
}