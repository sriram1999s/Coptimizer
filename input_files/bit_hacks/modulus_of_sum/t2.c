#include<stdio.h>

int main()
{
    int r = (2+3)%5;
    printf("%d\n", r);

    r = (2+ -1) % 5;
    printf("%d\n", r);

    r = (-2+ -1) % 5;
    printf("%d\n", r);

    r = (-2+ 1) % 5;
    printf("%d\n", r);

    r = (2+ 1) % -5;
    printf("%d\n", r);

    return 0;
}
