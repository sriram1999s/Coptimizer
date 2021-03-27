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
    foo1();
    foo5();
}

void foo5()
{
    int f5=5;
    foo3();
    foo2();
    foo1();
    foo6();
}

void foo6()
{
    int f6=6;
}

int main()
{
    foo1();
    return 0; 
}