#include<time.h>
#include<string.h>
#include<sys/resource.h>
#include <errno.h>
#include<stdio.h>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<sys/resource.h>
#include<errno.h>
int main()
{struct rusage r_usage;
	int n;
	int W;
	scanf("%d %d", &n, &W);
	int *wt = malloc(sizeof(int) * n);
	int *val = malloc(sizeof(int) * n);
	for (int j = 0; j < n; j++) {
		scanf("%d", &wt[j]);
	} for (int k = 0; k < n; k++) {
		scanf("%d", &val[k]);
	} int **K = malloc(sizeof(int *) * (n + 1));
	for (int p = 0; p < n + 1; ++p) {
		K[p] = malloc(sizeof(int) * (W + 1));
	} int c_i = 0;
	int c_w = 0;		double startTime = (float)clock()/CLOCKS_PER_SEC;
	int temp_46e8d8256240708200b54721b6fa46ab =
	    (((n + 1 - (0)) / 1) + (((n + 1 - (0)) % 1) != 0));
	int temp_loop_fcc49520abaf3b5e87b249cf70979065;
	for (int i = 0;
	     i <
	     (temp_46e8d8256240708200b54721b6fa46ab -
	      (temp_46e8d8256240708200b54721b6fa46ab % 2)) / 2; i++) { {
			temp_loop_fcc49520abaf3b5e87b249cf70979065 = i;
	} {
		c_w = 0;
		int temp_b2f37e64454a449c9d47a668c5cf5bd3 =
		    (((W + 1 - (0)) / 1) + (((W + 1 - (0)) % 1) != 0));
		int temp_loop_6ed487118ca183132c55be1ceece4e6a;
		for (int w = 0;
		     w <
		     (temp_b2f37e64454a449c9d47a668c5cf5bd3 -
		      (temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) / 2; w++) { {
				temp_loop_6ed487118ca183132c55be1ceece4e6a = w;
		} {
			if (c_i == 0 || c_w == 0) {
				K[c_i][c_w] = 0;
			} else if (wt[c_i - 1] <= c_w) {
				if (val[c_i - 1] +
				    K[c_i - 1][c_w - wt[c_i - 1]] >
				    K[c_i - 1][c_w]) {
					K[c_i][c_w] =
					    val[c_i - 1] + K[c_i - 1][c_w -
								      wt[c_i -
									 1]];
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
			} else {
				K[c_i][c_w] = K[c_i - 1][c_w];
			}
			c_w++;
		}
		{
			if (c_i == 0 || c_w == 0) {
				K[c_i][c_w] = 0;
			} else if (wt[c_i - 1] <= c_w) {
				if (val[c_i - 1] +
				    K[c_i - 1][c_w - wt[c_i - 1]] >
				    K[c_i - 1][c_w]) {
					K[c_i][c_w] =
					    val[c_i - 1] + K[c_i - 1][c_w -
								      wt[c_i -
									 1]];
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
			} else {
				K[c_i][c_w] = K[c_i - 1][c_w];
			}
			c_w++;
		}
		}
		if ((temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) { {
				if (c_i == 0 || c_w == 0) {
					K[c_i][c_w] = 0;
				} else if (wt[c_i - 1] <= c_w) {
					if (val[c_i - 1] +
					    K[c_i - 1][c_w - wt[c_i - 1]] >
					    K[c_i - 1][c_w]) {
						K[c_i][c_w] =
						    val[c_i - 1] + K[c_i -
								     1][c_w -
									wt[c_i -
									   1]];
					} else {
						K[c_i][c_w] = K[c_i - 1][c_w];
					}
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
				c_w++;
		}
		}
		c_i++;
	}
	{
		c_w = 0;
		int temp_b2f37e64454a449c9d47a668c5cf5bd3 =
		    (((W + 1 - (0)) / 1) + (((W + 1 - (0)) % 1) != 0));
		int temp_loop_6ed487118ca183132c55be1ceece4e6a;
		for (int w = 0;
		     w <
		     (temp_b2f37e64454a449c9d47a668c5cf5bd3 -
		      (temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) / 2; w++) { {
				temp_loop_6ed487118ca183132c55be1ceece4e6a = w;
		} {
			if (c_i == 0 || c_w == 0) {
				K[c_i][c_w] = 0;
			} else if (wt[c_i - 1] <= c_w) {
				if (val[c_i - 1] +
				    K[c_i - 1][c_w - wt[c_i - 1]] >
				    K[c_i - 1][c_w]) {
					K[c_i][c_w] =
					    val[c_i - 1] + K[c_i - 1][c_w -
								      wt[c_i -
									 1]];
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
			} else {
				K[c_i][c_w] = K[c_i - 1][c_w];
			}
			c_w++;
		}
		{
			if (c_i == 0 || c_w == 0) {
				K[c_i][c_w] = 0;
			} else if (wt[c_i - 1] <= c_w) {
				if (val[c_i - 1] +
				    K[c_i - 1][c_w - wt[c_i - 1]] >
				    K[c_i - 1][c_w]) {
					K[c_i][c_w] =
					    val[c_i - 1] + K[c_i - 1][c_w -
								      wt[c_i -
									 1]];
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
			} else {
				K[c_i][c_w] = K[c_i - 1][c_w];
			}
			c_w++;
		}
		}
		if ((temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) { {
				if (c_i == 0 || c_w == 0) {
					K[c_i][c_w] = 0;
				} else if (wt[c_i - 1] <= c_w) {
					if (val[c_i - 1] +
					    K[c_i - 1][c_w - wt[c_i - 1]] >
					    K[c_i - 1][c_w]) {
						K[c_i][c_w] =
						    val[c_i - 1] + K[c_i -
								     1][c_w -
									wt[c_i -
									   1]];
					} else {
						K[c_i][c_w] = K[c_i - 1][c_w];
					}
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
				c_w++;
		}
		}
		c_i++;
	}
	}
	if ((temp_46e8d8256240708200b54721b6fa46ab % 2)) { {
			c_w = 0;
			int temp_b2f37e64454a449c9d47a668c5cf5bd3 =
			    (((W + 1 - (0)) / 1) + (((W + 1 - (0)) % 1) != 0));
			int temp_loop_6ed487118ca183132c55be1ceece4e6a;
			for (int w = 0;
			     w <
			     (temp_b2f37e64454a449c9d47a668c5cf5bd3 -
			      (temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) / 2;
			     w++) { {
					temp_loop_6ed487118ca183132c55be1ceece4e6a
					    = w;
			} {
				if (c_i == 0 || c_w == 0) {
					K[c_i][c_w] = 0;
				} else if (wt[c_i - 1] <= c_w) {
					if (val[c_i - 1] +
					    K[c_i - 1][c_w - wt[c_i - 1]] >
					    K[c_i - 1][c_w]) {
						K[c_i][c_w] =
						    val[c_i - 1] + K[c_i -
								     1][c_w -
									wt[c_i -
									   1]];
					} else {
						K[c_i][c_w] = K[c_i - 1][c_w];
					}
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
				c_w++;
			}
			{
				if (c_i == 0 || c_w == 0) {
					K[c_i][c_w] = 0;
				} else if (wt[c_i - 1] <= c_w) {
					if (val[c_i - 1] +
					    K[c_i - 1][c_w - wt[c_i - 1]] >
					    K[c_i - 1][c_w]) {
						K[c_i][c_w] =
						    val[c_i - 1] + K[c_i -
								     1][c_w -
									wt[c_i -
									   1]];
					} else {
						K[c_i][c_w] = K[c_i - 1][c_w];
					}
				} else {
					K[c_i][c_w] = K[c_i - 1][c_w];
				}
				c_w++;
			}
			}
			if ((temp_b2f37e64454a449c9d47a668c5cf5bd3 % 2)) { {
					if (c_i == 0 || c_w == 0) {
						K[c_i][c_w] = 0;
					} else if (wt[c_i - 1] <= c_w) {
						if (val[c_i - 1] +
						    K[c_i - 1][c_w -
							       wt[c_i - 1]] >
						    K[c_i - 1][c_w]) {
							K[c_i][c_w] =
							    val[c_i - 1] +
							    K[c_i - 1][c_w -
								       wt[c_i -
									  1]];
						} else {
							K[c_i][c_w] =
							    K[c_i - 1][c_w];
						}
					} else {
						K[c_i][c_w] = K[c_i - 1][c_w];
					}
					c_w++;
			}
			}
			c_i++;
	}
	}			double endTime = (float)clock()/CLOCKS_PER_SEC; double timeElapsed = endTime - startTime;
	printf("%d\n", K[n][W]);

int ret = getrusage(RUSAGE_SELF,&r_usage);FILE *fp = fopen("profile","w");
if(ret == 0)
fprintf(fp,"%ld\n",r_usage.ru_maxrss);
else
fprintf(fp,"%d\n", -1);fprintf(fp,"%f\n",timeElapsed); fclose(fp);}
