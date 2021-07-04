#include<stdio.h>
int foo(int x)
{
    return x + ( x * 20 ) - 30;
}

int main(){
    int A;
    A = foo(2);
}
