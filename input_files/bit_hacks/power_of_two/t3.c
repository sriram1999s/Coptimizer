#include<stdio.h>
#include<stdbool.h>

bool powerOf2(int n)
{
	/*power-of-2-begin*/
	if (n == 1)
	return true;

	else if (n % 2 != 0 || n ==0)
	return false;

	return powerOf2(n / 2);
	/*power-of-2-end*/
}

// Driver Code
int main()
{
	int n = 64;//True
	int m = 12;//False

	if (powerOf2(n) == 1)
	    printf("Yes\n");

	else
	    printf("No\n");

	if (powerOf2(m) == 1)
	    printf("Yes\n");

	else
        printf("No\n");
}