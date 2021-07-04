#include<stdio.h>

int main() {
    double powers_2[32];
    double mul_2[32];
    for(int i=0;i<31;i++) {  
	powers_2[i] = 1<<i;
    }

    for(int i=0;i<31;i++) {
	mul_2[i] = 2*i;
    }
    double sum_pow = 0;
    double sum_mul = 0;
    int n;
    
    printf("Provide a positive integer less than 30: \n");
    scanf("%d",&n);
    int c_j = 0;
    int c_k = 0;
    
    for(int j=0;j<n;j++) {
	sum_pow += powers_2[c_j];
	c_j += 1;
    }
    
    for(int k=0;k<n;k++) {
	sum_mul += mul_2[c_k]; 
	c_k += 1;
    }

    printf("sum of powers of 2 : %lf\n",sum_pow);
    printf("sum of multiples of 2: %lf\n",sum_mul);
}
	   

    

    
