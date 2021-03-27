void foo1();
void foo2();
void foo3();
void foo4();
void foo5();
void foo6();
void foo7();
void foo8();
void foo9();
void foo10();
void foo11();

void foo1()
{
    foo11();
    foo2();
}

void foo2()
{
    foo3();
}

void foo3()
{
    foo4();
    foo10();
}

void foo4()
{
    foo9();
    foo5();
    foo7();
}

void foo5()
{
    foo6();
}

void foo6()
{
    foo7();
    foo8();
    foo1();
}

void foo7()
{
    foo3();
    int f7=7;
}

void foo8()
{
    int f8=8;
    foo11();
}

void foo9()
{
    int f9=9;
}

void foo10()
{
    int f10=10;
}

void foo11()
{
    int f11=11;
}

void main()
{
    foo6();
}