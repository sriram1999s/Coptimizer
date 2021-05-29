void foo1();
void foo2();
void foo3();
void foo4();

void foo5();
void foo6();
void foo7();
void foo8();

void foo1()
{
    int f1=1;
    foo2();
    foo4();
}

void foo2()
{
    int f2=1;
    foo3();
}

void foo3()
{
    int f3=1;
    foo1();
}

void foo4()
{
    int f4=1;
    foo5();
}


void foo5()
{
    int f5=1;
}

void foo6()
{
    int f6=1;
    foo5();
    foo7();
}

void foo7()
{
    int f7=1;
    foo8();
}

void foo8()
{
    int f8=1;
    foo6();
}

void main()
{
    foo1();
}