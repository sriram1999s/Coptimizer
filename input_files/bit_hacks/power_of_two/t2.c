#include<stdio.h>

bool isPowerOfTwo(int n)
{
    /*power-of-2-begin*/
	if (n == 0)
		return 0;
	while (n != 1)
	{
		if (n%2 != 0)
			return 0;
		n = n/2;
	}
	return 1;
	/*power-of-2-end*/
}

int main()
{
    if(isPowerOfTwo(31))
    {
        printf("Yes\n");
    }
    else
    {
        printf("No\n");
    }


    if(isPowerOfTwo(64))
    {
        printf("Yes\n");
    }
    else
    {
        printf("No\n");
    }
    return 0;
}
