#include <stdio.h>

int countSetBits(int num)
{
    /*count-set-bits-begin*/
	int count = 0;
	while (num) {
		num &= (num - 1);
		count++;
	}
	return count;
	/*count-set-bits-end*/
}

int main()
{
	int i = 9;
	printf("%d", countSetBits(i));
	return 0;
}
