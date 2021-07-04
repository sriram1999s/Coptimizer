#include <stdio.h>
int main() {
   int i;
   int j;
   int rows;
   int a = 0;
   printf("Enter the number of rows: \n");
   scanf("%d", &rows);
   for (i = 1; i <= rows; ++i) {
      for (j = 1; j <= i; ++j) {
         printf("* ");
      }
      printf("\n");
   }
}
