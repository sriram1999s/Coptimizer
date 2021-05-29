#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<sys/resource.h>
#include<errno.h>

int main() {
    int n;
    int W;
    scanf("%d %d",&n,&W);
    int* wt = malloc(sizeof(int)*n);
    int* val = malloc(sizeof(int)*n);

    for(int j=0;j<n;j++) {
	scanf("%d",&wt[j]);
    }
    for(int k=0;k<n;k++) {
	scanf("%d",&val[k]);
    }

    int **K = malloc(sizeof(int*)*(n+1));
    for(int p=0;p<n+1;++p) {
	K[p] =  malloc(sizeof(int)*(W+1));
    }

    int c_i=0;
    int c_w=0;

    /* TIME_1 */

    for (int i = 0; i <= n; i++)
        {
	    c_w=0;
            for (int w = 0; w <= W; w++)
            {
                if (c_i == 0 || c_w == 0) {
                    K[c_i][c_w] = 0;
                } else if (wt[c_i - 1] <= c_w) {
                    if(val[c_i-1]+K[c_i-1][c_w-wt[c_i-1]]>K[c_i-1][c_w]) {
                        K[c_i][c_w] = val[c_i-1]+K[c_i-1][c_w-wt[c_i-1]];
                    }
                    else {
                         K[c_i][c_w] = K[c_i-1][c_w];
                    }
                }
                else {
                    K[c_i][c_w] = K[c_i - 1][c_w];
		}
		c_w++;
            }
	    c_i++;
        }

    /* TIME_2 */
    
    printf("%d\n",K[n][W]);

    
}
