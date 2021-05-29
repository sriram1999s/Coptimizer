void foo(int f)
{
    f = 1;
}

int bar(int b1, int b2)
{
    int b = b1+b2;
    return b;
}

float goo(int g1, float g2, float g3)
{
    float prod = g2*g3;
    float sum = prod + g1;
    return sum;
}

int main()
{

    int g11=10;
    float g22=0.5;
    float g33=1.0;
    foo(g22/((g22+g33)*g33));
    int res_bar = bar(1, 2);
    float res_goo = goo(g11, g22+g33, g33);
    return 0;
}
