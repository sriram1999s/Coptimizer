#include<stdio.h>
#include<stdbool.h>
#include<math.h>

bool isPowerOfTwo(int n)
{
    /*power-of-2-begin*/
   if(n==0)
   return false;

   return (ceil(log2(n)) == floor(log2(n)));
   /*power-of-2-end*/
}

int main()
{
    if(isPowerOfTwo(31))
        printf("Yes\n");
    else
        printf("No\n");

    if(isPowerOfTwo(64))
        printf("Yes\n");
    else
        printf("No\n");
    return 0;
}
