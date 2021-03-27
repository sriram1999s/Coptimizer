int foo()
{
    if(0<1)
        return 1;
    else
    {
        return 0;
    }
}

int bar()
{
    return 1;
    int a = 5;
    return a;
}

void main()
{
    int res_foo = foo();
    int res_bar = bar();
}