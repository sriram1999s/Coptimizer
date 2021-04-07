#include<stdio.h>
#include<time.h>

void foo1();
void foo2();
void foo3();
void foo4();
void foo5();
void foo6();

void foo1()
{
    int f1=1;
    foo2();
}


void foo2()
{
    int f2=2;
    foo3();
}

void foo3()
{
    int f3=3;
    foo4();
}

void foo4()
{
    int f4=4;
    foo5();
}

void foo5()
{
    int f5=5;
    foo6();
}

void foo6()
{
    int f6=6;
}

int main()
{
    double startTime = (float)clock()/CLOCKS_PER_SEC;
    foo1();
    double endTime = (float)clock()/CLOCKS_PER_SEC;
    double timeElapsed = endTime - startTime;
    printf("%d\n", 1);
    printf("%lf\n",timeElapsed);
    return 0; 
}
