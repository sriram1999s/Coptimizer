# include <stdio.h>

int main()
{
    int a=1, b, c;
    scanf("%d", &b);
    scanf("%d", &c);

    if(a>=0 && a<1)
    {
        printf("zero");
    }
    else if(a>=1 && a<2)
    {
        printf("one");
    }

    if(b>=0 && b<=0)
    {
        printf("b zero");
    }
    else if(b>=1 && b<=1)
    {
        printf("b one");
    }

    
    if(c>15 && c<=20)
    {
        printf("c four");
    }
    else if(c>0 && c<=5)
    {
        printf(" c one");
    }
    else if(c>10 && c<=15)
    {
        printf("c three");
    }
    else if(c>5 && c<=10)
    {
        printf("c two");
    }

}
