#include<stdio.h>

int main()
{
    int arr[10] = {2, 0, 1, 3, 13, 11, 7, 8, 9, 10};
    int min_ele;        //0,0,1,3
    for(int i=0; i<9; ++i)
    {
        if(arr[i]<arr[i+1]) {
            min_ele = arr[i];
        }
        else {
            min_ele = arr[i+1];
        }
        printf("%d\n", min_ele);
    }
}