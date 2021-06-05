void foo(int f1, int f2, int f3)
{
    int f = f2+f3-f1;
}

int main()
{
    foo(1,2,3);
    float t = 1.0;
    foo(10, 20, 30);
    float t1 = 2.0;
    foo(100,200,300);
}
