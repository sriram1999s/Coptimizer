// Count number of bits to be flipped
// to convert A into B
#include <stdio.h>

int countSetBits(int N)
{
    /*count-set-bits-begin*/
	int count = 0;
    int i = 0;
    while(i < sizeof(int) * 8) {
        if (N & (1 << i))
        {
            count++;
        }
        ++i;
    }
    return count;
	/*count-set-bits-end*/
}

// Driver code
int main()
{
	int i = 9;
	printf("%d", countSetBits(i));
	return 0;
}
