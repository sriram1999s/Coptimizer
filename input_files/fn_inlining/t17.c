void foo1();
void foo2();
void foo3();
void foo4();

void foo1()
{
    int f1=1;
    foo2();
}


void foo2()
{
    int f2=2;
    if(0)
        return foo3();
    else
        return foo4();
}

void foo3()
{
    int f3=3;
    foo1();
}

void foo4()
{
    int f4=4;
    foo3();
}

void main()
{
    foo1();
    foo2();
}