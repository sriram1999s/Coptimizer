#include <stdio.h>

void sum(int size, double sum1)
{
    if (size == 0)
    {
        printf("sum : %f\n",sum1);
    }
    else { sum(size - 1, sum1 + size);
}
}

int main()
{
    int size = 100000;
    sum(size, 0);
    return 0;
}
