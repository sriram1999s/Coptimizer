#include<stdio.h>

int main()
{
    int a = 2, b=3;
    int *p=&a;
    int *q=&b;
    int r;
    if(*p<*q)
    {
        r = *p;
    }
    else
    {
        r = *q;
    }
    printf("%d", r);
    return 0;
}