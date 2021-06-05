#include <stdio.h>

int main()
{
    int var1, var2, var3;
    scanf("%d", &var1);
    scanf("%d", &var2);
    scanf("%d", &var3);
    if(var1==0)
    {
        printf("var1 is 0");
    }
    else if(var1==1)
    {
        printf("var1 is 1");
    }
    else if(var1==2)
    {
        printf("var1 is 2");
    }
    else if(var1==3)
    {
        printf("var1 is 3");
    }
    else if(var1==4)
    {
        printf("var1 is 4");
    }
    else if(var1==5)
    {
        printf("var1 is 5");
    }
    else if(var1==6)
    {
        printf("var1 is 6");
    }
    else if(var1==7)
    {
        printf("var1 is 7");
    }
    else if(var1==8)
    {
        printf("var1 is 8");
    }
    else if(var1==9)
    {
        printf("var1 is 9");
    }
    else if(var1==10)
    {
        printf("var1 is 10");
    }
    else if(var1==11)
    {
        printf("var1 is 11");
    }
    else if(var1==12)
    {
        printf("var1 is 12");
    }
    else if(var1==13)
    {
        printf("var1 is 13");
    }
    else if(var1==14)
    {
        printf("var1 is 14");
    }
    else if(var1==15)
    {
        printf("var1 is 15");
        if(var2==0 && var3<10)
        {
            printf("var2 is 0, var3 is less than 10");
        }
        else if(var2==1 && var3>=10 && var3<20)
        {
            printf("var2 is 1, var3 is between 9 and 20");
        }
        else if(var2==2 && var3>=10 && var3<20)
        {
            printf("var2 is 2, var3 is between 9 and 20");
        }
        else if(var2==3 && var3<10)
        {
            printf("var2 is 3, var3 is less than 10");
        }
        else if(var2==4 && var3<10)
        {
            printf("var2 is 4, var3 is less than 10");
        }
        else if(var2==5 && var3>=10 && var3<20)
        {
            printf("var2 is 5, var3 is between 9 and 20");
        }
        else if(var2==6)
        {
            printf("var2 is 6");
        }
        else if(var2==7)
        {
            printf("var2 is 7");
        }
        else if(var2==8)
        {
            printf("var2 is 8");
        }
        else if(var2==9)
        {
            printf("var2 is 9");
        }
        else if(var2==10)
        {
            printf("var2 is 10");
        }
        else if(var2==11)
        {
            printf("var2 is 11");
        }
        else if(var2==12)
        {
            printf("var2 is 12");
        }
        else if(var2==13)
        {
            printf("var2 is 13");
        }
        else if(var2==14)
        {
            printf("var2 is 14");
        }
        else if(var2==15)
        {
            printf("var2 is 15");
        }
        else if(var2==16)
        {
            printf("var2 is 16");
        }
        else if(var2==17)
        {
            printf("var2 is 17");
        }
        else if(var2==18)
        {
            printf("var2 is 18");
        }
        else if(var2==19)
        {
            printf("var2 is 19");
        }
        else if(var2==20)
        {
            printf("var2 is 20");
            int i=0;
            while(i<10)
            {
                if(var3==10)
                {
                    printf("var3 is 10");
                }
                else if(var3==20 || var3==30)
                {
                    printf("var3 is 20 or 30");
                }
                else if(var3==40)
                {
                    printf("var3 is 40");
                }
                else if(var3==50)
                {
                    printf("var3 is 50");
                }
                else
                {
                    printf("var3 other");
                }
                printf("chain 2 in while\n");
                if(var3==10)
                {
                    printf("var3 is 10");
                }
                else if(var3==20)
                {
                    printf("var3 is 20");
                }
                else if(var3==40)
                {
                    printf("var3 is 40");
                }
                else if(var3==50)
                {
                    printf("var3 is 50");
                }
                else
                {
                    printf("var3 other");
                }
                i++;
            }
        }
    }
    else
    {
        printf("other");
    }
}
