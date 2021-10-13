// sort an array of unique positive integers
#include<stdio.h>

void counting_sort(int *array, int n)
{
    /*sort-positive-begin*/
    /*(array,n)*/
    int output[n];

    int max = array[0];
    for (int i = 1; i < n; i++) {
        if (array[i] > max) {
            max = array[i];
        }
    }

    int count[n];
    for (int i = 0; i <= max; ++i) {
        count[i] = 0;
    }

    for (int i = 0; i < n; i++) {
        count[array[i]]++;
    }

    for (int i = 1; i <= max; i++) {
        count[i] += count[i - 1];
    }

    for (int i = n - 1; i >= 0; i--) {
        output[count[array[i]] - 1] = array[i];
        count[array[i]]--;
    }

    for (int i = 0; i < n; i++) {
        array[i] = output[i];
    }
    /*sort-positive-end*/
}

void display(int* arr, int n)
{
    for(int i=0; i<n; ++i)
    {
        printf("%d ", arr[i]);
    }
}

int main()
{
    int arr[] = {2, 1, 3, 3, 2, 3};
    int n = sizeof(arr)/sizeof(int);
    counting_sort(arr, n);
    display(arr, n);
    return 0;
}