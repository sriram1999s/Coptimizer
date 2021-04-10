#include<time.h>
#include<string.h>
#include<stdio.h>
void looping(int n)
{
    int a = 0;
    int temp_1edebf30e10bb1615c508e011c631bba =
	(((n - (0)) / 1) + (((n - (0)) % 1) != 0));
    for (int i = 0;
	 i <
	 (temp_1edebf30e10bb1615c508e011c631bba -
	  (temp_1edebf30e10bb1615c508e011c631bba % 2)) / 2; i++) { {
	    a++;
    } {
	a++;
    }} if ((temp_1edebf30e10bb1615c508e011c631bba % 2)) { {
	    a++;
    }
    }
    printf("%d\n", a);
}

int main()
{double startTime = (float)clock()/CLOCKS_PER_SEC;{
    int n1;
    int n2;
    int n3;
    scanf("%d", &n1);
    scanf("%d", &n2);
    scanf("%d", &n3);
    looping(n1);
    looping(n2);
    looping(n3);double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime; FILE *fp = fopen("profile","w"); fprintf(fp,"%f\n",timeElapsed); fclose(fp);}}

