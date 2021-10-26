#include<stdio.h>

int num_to_bits[16] = { 0, 1, 1, 2, 1, 2, 2, 3,
                        1, 2, 2, 3, 2, 3, 3, 4 };

int countSetBits(int num)
{
    int nibble=0;
    /*count-set-bits-begin*/
	if (0 == num){
	    return num_to_bits[0];
	}
    nibble = num & 2;
    return num_to_bits[nibble] + countSetBitsRec(num >> 4);
    /*count-set-bits-end*/
}

int main()
{
	int i = 9;
	printf("%d", countSetBits(i));
	return 0;
}
