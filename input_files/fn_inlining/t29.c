void foo1();
void foo2();
void foo3();
void foo4();
void foo5();

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
    foo2();
}

void main()
{
    foo1();
}


