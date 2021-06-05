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
    foo2();
    foo5();
}

void foo2()
{
    foo3();
}

void foo3()
{
    foo4();
}

void foo4()
{
    foo1();
}

void foo5()
{
    foo6();
}

void foo6()
{
    foo7();
}

void foo7()
{
    foo8();
}

void foo8()
{
    foo1();
}

void main()
{
    foo3();
}