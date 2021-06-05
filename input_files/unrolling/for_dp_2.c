#include<stdio.h>
#include<stdlib.h>

int main() {
    int n;
    int W;
    scanf("%d %d",&n,&W);
    int wt[n];
    int val[n];
    int x;
    for(int j=0;j<n;j++) {
	scanf("%d",&x);
	wt[j] = x;
    }
    for(int k=0;k<n;k++) {
	scanf("%d",&x);
	val[k] = x;
    }

    int K[n+1][W+1];

    int c_i=0;
    int c_w=0;

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
    printf("%d\n",K[n][W]);
    
}
