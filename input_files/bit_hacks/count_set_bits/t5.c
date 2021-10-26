// Count number of bits to be flipped
// to convert A into B
#include <stdio.h>

int countSetBits(int n)
{
    /*count-set-bits-begin*/
	int count = 0;
	while (n > 0)
	{
		count++;
		n &= (n-1);
	}
	return count;
	/*count-set-bits-end*/
}

// Function that return count of
// flipped number
int FlippedCount(int a, int b)
{
	// Return count of set bits in
	// a XOR b
	return countSetBits(a^b);
}

// Driver code
int main()
{
	int a = 10;
	int b = 20;
	printf("%d\n", FlippedCount(a, b));
	return 0;
}
