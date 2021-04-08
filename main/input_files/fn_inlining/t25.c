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
    foo5();
}

void foo5()
{
    foo6();
}

void foo6()
{
    foo7();
    foo1();
    foo8();
}

void foo7()
{
    int f7=7;
}

void foo8()
{
    int f8=8;
}

int main()
{
    foo6();
}