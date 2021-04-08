#include<stdio.h>
void sum(int size, double sum1)
{
  label_1306ffc245ec4396a2ba688429dae523:{
    }
    if (size == 0) {
	printf("sum : %f\n", sum1);
    } else { {			// tail recursion eliminated
	    int par_size_1306ffc245ec4396a2ba688429dae523 = size;
	    double par_sum1_1306ffc245ec4396a2ba688429dae523 = sum1;
	    size = par_size_1306ffc245ec4396a2ba688429dae523 - 1;
	    sum1 =
		par_sum1_1306ffc245ec4396a2ba688429dae523 +
		par_size_1306ffc245ec4396a2ba688429dae523;
	    goto label_1306ffc245ec4396a2ba688429dae523;
    };
    }
    return;
}

int main()
{
    int size = 100000;
    sum(size, 0);
    return 0;
}
