#include<stdio.h>

int main()
{
    int res, n=20;
    /*power-of-2-begin*/
	if (n == 0)
	{
	    res = 0;
	}
	else
	{
	    while (n != 1)
        {
            if (n%2 != 0)
            {
                res = 0;
                break;
            }
            n = n/2;
        }
        res = 1;
	}
	/*power-of-2-end*/
	if(res)
	{
	    printf("Yes\n");
	}
    else
    {
        printf("No\n");
    }
    return 0;
}
