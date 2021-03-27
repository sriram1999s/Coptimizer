int rec_func(int a)
{
    if(a<=0) {
        return 0;
}
    return rec_func(a);
}

int rec_func2(int q,int *p,double *r)
{
    int z;
    return z;
}
int main()
{
    int a = 10;
    int b = 100;
    a = a-1;
    int res = rec_func(10);
    int a1[3] = {1,2,3};
    int a2[10];
    double a3[10];
    res = rec_func2(a1[2],a1 + 3,a3);
}
