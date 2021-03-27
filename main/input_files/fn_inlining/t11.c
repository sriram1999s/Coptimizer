int rec_func(int a)
{
    if(a<=0)
        return 0;
    return rec_func(a);
}

int rec_func2(int a)
{
    if(a<=0)
        return 0;
    a = a-1;
    return rec_func(a);
}

void main()
{
    int res = rec_func(10);
    res = rec_func2(10);
}