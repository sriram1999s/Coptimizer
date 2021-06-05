int foo()
{
    int b = rec_func(0);
    int f = b+10;
    return f;
}

int bar()
{
    return 1;
}

int rec_func(int a)
{
    int x; 
    if(a<=0)
        return 0;
    x = bar();
    return rec_func(a);
}

void main()
{
    int ret_foo = foo();
}