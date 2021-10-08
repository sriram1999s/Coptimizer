#include<stdio.h>

void counting_sort(int *array, int n)
{
    /*count-sort-unique-begin*/
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
    /*count-sort-unique-end*/
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
    int arr[] = {3, 6, 1, 2, 7, 9, 5, 8, 0, 4};
    int n = sizeof(arr)/sizeof(int);
    counting_sort(arr, n);
    display(arr, n);
    return 0;
}