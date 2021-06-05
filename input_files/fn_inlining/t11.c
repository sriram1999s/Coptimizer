
int rec_func(int a)
{

    for(int j = 1;j<3;)
    {
      j = (5*5) - (5*5) + 1 + j;
    }
    if(a<=0) {
        return 0;
    }
    else if(a<=5)
    {
      int x;
      x = 100;
      x = x * 4;
      rec_func(a);
      printf("%d\n",x);
    }
    else if(a<=10) { return rec_func(a);}
    else {  rec_func(a);}
    int x = 100;
    
    rec_func(a);

}

int rec_func3()
{
  int x = 10;
  rec_func3();
  x++;
  printf("%d\n",x);
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
