#include<stdio.h>
#include<stdlib.h>

int main()
{
    int arr[3] = {10, -1, 0};
    int n = sizeof(arr)/sizeof(int);
    for(int i=0; i<n; ++i)
        printf("Abs of %d is %d\n", arr[i], abs(arr[i]));
    return 0;
}