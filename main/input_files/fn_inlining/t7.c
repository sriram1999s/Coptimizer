#include<stdio.h>
#include<time.h>

int foo()
{
    if(0<1) {
        return 1;
    } else
    {
        return 0;
    }
}

int bar()
{
    int a = 5;
    return a;
}

int main()
{
    double startTime = (float)clock()/CLOCKS_PER_SEC;
    int res_foo = foo();
    int res_bar = bar();
    double endTime = (float)clock()/CLOCKS_PER_SEC;
    double timeElapsed = endTime - startTime;
    printf("%d\n", 1);
    printf("%lf\n",timeElapsed);
}
