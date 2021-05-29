
int bar()
{
    goo();
    return 1;
}

void goo()
{
    float g=2.5;
    int b = bar();
}

void main()
{
    int ret_foo = bar();
}
