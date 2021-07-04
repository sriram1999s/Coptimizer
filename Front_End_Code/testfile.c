#include<stdio.h>
int get_square(int num)
{
    return num * num;
}
int get_cube(int num)
{
    /* find square of 'num' */

    int square_num = get_square(num);
    return square_num * num;
}

int main()
{
    /* prog. to find cube of 'num'  */

    int num;
    scanf("%d", &num);
    int cube_num = get_cube(num);
    printf("The cube of num : %d\n", cube_num);
    return 0;
}
