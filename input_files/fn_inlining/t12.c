int foo()
{
    int b = bar();
    int f = b+10;
    return f;
}

int bar()
{
    goo();
    return 1;
}

void goo()
{
    float g=2.5;
}

void main()
{
    int ret_foo = foo();

}
