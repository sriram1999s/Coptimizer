int foo1();
int foo2();
int foo3();

int foo1()
{
    return foo2();
}

int foo2()
{
    if(0)
        return foo3();
    else
        return foo1();
}

int foo3()
{
    int x;
    return x+(x*20);
}

void foox(int p,float q)
{
  p = p - 1;
}
void main()
{
    foo2();
    foox(10,20);
}
