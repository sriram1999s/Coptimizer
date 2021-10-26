#include<stdio.h>

int main()
{
    int x = 6, y= 2, z=0, n = 10;
    int r = ((x+y)%n + z)%n;
    printf("%d\n", r);
    return 0;
}