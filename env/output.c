#include<stdio.h>
int check_overlap(int x1, int y1, int x2, int y2)
{
	if (x1 > y1 || x2 > y2)
		return 0;
	if ((x1 >= x2 && x1 < y2) || (y1 > x2 && y1 <= y2)
	    || ((x1 < y1 ? x1 : y1) > (x2 < y2 ? x2 : y2)
		&& (x1 > y1 ? x1 : y1) < (x2 > y2 ? x2 : y2))
	    || ((x1 < y1 ? x1 : y1) < (x2 < y2 ? x2 : y2)
		&& (x1 > y1 ? x1 : y1) > (x2 > y2 ? x2 : y2)))
		return 1;
	return 0;
}

int main()
{
	int n;
	scanf("%d", &n);	/* n = 4 */
	int a = 0;
	int b = 0;
	int c = 0;
	for (int i = 0; i < n; i++) {	/* [0,4) */
		if (check_overlap(i + 1, n, i + 2 + 1, n - 1 + 1)) {
			int temp_b45ce20f2924 =
			    (i + 1 < i + 2 + 1 ? i + 1 : i + 2 + 1);
			int temp_13702ee525ac = (n < n - 1 + 1 ? n : n - 1 + 1);
			int temp_b5aea6cb850b =
			    (i + 1 > i + 2 + 1 ? i + 1 : i + 2 + 1);
			int temp_94c5281cda92 = (n > n - 1 + 1 ? n : n - 1 + 1);
			for (int j = temp_b5aea6cb850b; j < temp_13702ee525ac; j += 1) { {	/* [i+1,4) */
					a++;
			} {	/* [i+2,n-1)    i+3-n */
				b++;
			}} for (int j = 0;
				j < (temp_b5aea6cb850b - temp_b45ce20f2924);
				j += 1) {
				if (temp_b45ce20f2924 == i + 2 + 1) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
			for (int z = 0;
			     z < (temp_94c5281cda92 - temp_13702ee525ac); z++) {
				if (temp_94c5281cda92 == n - 1 + 1) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
		} else {
			for (int j = i + 1; j < n; j += 1) {	/* [i+2,n-1)    i+3-n */
				b++;
			} for (int j = i + 2 + 1; j < n - 1 + 1; j += 1) {	/* [i+1,4) */
				a++;
	}}} for (int i = 1; i < n - 1; i++) {
		c++;
	} printf("%d %d %d\n", a, b, c);
}
