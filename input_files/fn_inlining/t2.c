void foo()
{
    int f1 = 1;
    return;
    return;
}

int bar()
{
    int b1 = 1;
    return b1;
}

int goo()
{
    int g1 = 1;
    return g1;
}

int main()
{
    foo();
    int res_bar = bar();
    int res_goo;
    res_goo = goo();
    return 0;
}
