#include<stdio.h>
#include<stdlib.h>

void func(int r)
{
    printf("%d\n", r);
}

int main()
{
    int x = -2;
    int r = abs(x);
    printf("%d\n", r);

    r = abs(-11);
    printf("%d\n", r);

    r = abs(x-10);
    printf("%d\n", r);

    func(abs(10));
    return 0;
}