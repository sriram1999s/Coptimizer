# include <stdio.h>

int main()
{
    int a=1;
    if(0<=a && a<10)
    {
        printf("0 to 9");
    }
    else if(a>=10 && a<20)
    {
        printf("10 to 19");
    }
    else if(20<=a && 30>a)
    {
        printf("20 to 29");
    }
    else if(a>=30 && 40>a)
    {
        printf("30 to 39");
    }
    else if(a<50 && 40<=a)
    {
        printf("40 to 49");
    }
    else if(a<60 && a>=50)
    {
        printf("50 to 59");
    }
    else if(70>a && 60<=a)
    {
        printf("60 to 69");
    }
    else if(80>a && a>=70)
    {
        printf("70 to 79");
    }
    else
    {
        printf("other");
    }

    int b;
    scanf("%d", &b);
    if(2<=b && b<6)
    {
        printf("2 to 5");
    }
    else if(b>=6 && b<10)
    {
        printf("6 to 9");
    }
    else if(10<=b && 14>b)
    {
        printf("10 to 13");
    }
    else if(b>=14 && 18>b)
    {
        printf("14 to 17");
    }
    else if(b<22 && 18<=b)
    {
        printf("18 to 21");
    }
    else if(b<26 && b>=22)
    {
        printf("22 to 25");
    }
    else if(30>b && 26<=b)
    {
        printf("26 to 29");
    }
    else if(34>b && b>=30)
    {
        printf("30 to 33");
    }
    else
    {
        printf("other2");
    }

    int c;
    scanf("%d", &c);
    if(-50<=c && c<-40)
    {
        printf("-50 to -41");
    }
    else if(c>=-40 && c<-30)
    {
        printf("-40 to -31");
    }
    else if(-30<=c && -20>c)
    {
        printf("-30 to -21");
    }
    else if(c>=-20 && -10>c)
    {
        printf("-20 to -11");
    }
    else if(c<0 && -10<=c)
    {
        printf("-10 to -1");
    }
    else if(c<10 && c>=0)
    {
        printf("0 to 9");
    }
}