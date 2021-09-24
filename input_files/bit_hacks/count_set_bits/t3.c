#include <stdio.h>

int countSetBits(int n)
{
    /*count-set-bits-begin*/
	if (n == 0){
	    return 0;
	}

    else{
        return 1 + countSetBits(n & (n - 1));
    }
	/*count-set-bits-end*/
}

int main()
{
	int i = 9;
	printf("%d", countSetBits(i));
	return 0;
}
