#include<stdio.h>
#include<time.h>

int foo1();
int foo2();
int foo3();

int foo1()
{
    return foo2();
}

int foo2()
{
    if(0) {
        return foo3();
    } else {
        return foo1();
}
}

int foo3()
{
    int x;
    return x+(x*20);
}

void foox(int p,float q)
{
  p = p - 1;
}
int main()
{
    double startTime = (float)clock()/CLOCKS_PER_SEC;
    foo2();
    foox(10,20);
    double endTime = (float)clock()/CLOCKS_PER_SEC;
    double timeElapsed = endTime - startTime;
    printf("%d\n",1);
    printf("%lf\n",timeElapsed);
}
