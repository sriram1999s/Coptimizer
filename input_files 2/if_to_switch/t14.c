# include <stdio.h>

int main()
{
    int a=1;
    if(-1<a && a<=9)
    {
        printf("0 to 9");
    }
    else if(a>9 && a<=19)
    {
        printf("10 to 19");
    }
    else if(19<a && 29>=a)
    {
        printf("20 to 29");
    }
    else if(a>29 && 39>=a)
    {
        printf("30 to 39");
    }
    else if(a<=49 && 39<a)
    {
        printf("40 to 49");
    }
    else if(a<=59 && a>49)
    {
        printf("50 to 59");
    }
    else if(69>=a && 59<a)
    {
        printf("60 to 69");
    }
    else if(79>=a && a>69)
    {
        printf("70 to 79");
    }
    else
    {
        printf("other");
    }

    int b;
    scanf("%d", &b);
    if(1<b && b<=5)
    {
        printf("2 to 5");
    }
    else if(b>5 && b<=9)
    {
        printf("6 to 9");
    }
    else if(9<b && 13>=b)
    {
        printf("10 to 13");
    }
    else if(b>13 && 17>=b)
    {
        printf("14 to 17");
    }

    int c;
    scanf("%d", &c);
    if(-51<c && c<=-41)
    {
        printf("-50 to -41");
    }
    else if(c>-41 && c<=-31)
    {
        printf("-40 to -31");
    }
    else if(-31<c && -21>=c)
    {
        printf("-30 to -21");
    }
    else if(c>-21 && -11>=c)
    {
        printf("-20 to -11");
    }
    else if(c<=-1 && -11<c)
    {
        printf("-10 to -1");
    }
    else if(c<=9 && c>-1)
    {
        printf("0 to 9");
    }
}