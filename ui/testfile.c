#include <stdio.h>
double sum(int n);

int main() {
    int number;
    double result;

    printf("Enter a positive integer : ");
    scanf("%d", &number);

    result = sum(number);

    printf("sum = %f\n", result);
    return 0;
}

double sum(int n) {
    if (n != 0) {
        // sum() function calls itself
        return n + sum(n-1); 
    } else {
        return n;
}
}



