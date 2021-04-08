int foo1();
int foo2();
int foo3();
int foo4();

int foo1()
{
    int x; 
    int f1=1;
    x  = foo2();
}


int foo2()
{
    int f2=2;
    if(0) {
        return foo3();
    } else {
        return foo4();
}
}

int foo3()
{
    int f3=3;
    return foo1();
}

int foo4()
{
    int f4=4;
    return foo3();
}

int main()
{
    foo1();
    int x = foo2();
    return 0; 
}
