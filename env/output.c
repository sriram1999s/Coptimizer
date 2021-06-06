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
		if (check_overlap(i + 2 + 1, n - 1 + 1, i + 1, n)) {
			int temp_870b1f7c2abf =
			    (i + 2 + 1 < i + 1 ? i + 2 + 1 : i + 1);
			int temp_05fba5751808 = (n - 1 + 1 < n ? n - 1 + 1 : n);
			int temp_065a2058eac0 =
			    (i + 2 + 1 > i + 1 ? i + 2 + 1 : i + 1);
			int temp_55be130ff850 = (n - 1 + 1 > n ? n - 1 + 1 : n);
			for (int j = temp_065a2058eac0; j < temp_05fba5751808; j += 1) { {	/* [i+1,4) */
					a++;
			} {	/* [i+2,n-1)    i+3-n */
				b++;
			}} for (int j = 0;
				j < (temp_065a2058eac0 - temp_870b1f7c2abf);
				j += 1) {
				if (temp_870b1f7c2abf == i + 1) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
			for (int z = 0;
			     z < (temp_55be130ff850 - temp_05fba5751808); z++) {
				if (temp_55be130ff850 == n) { {	/* [i+1,4) */
						a++;
				}
				} else { {	/* [i+2,n-1)    i+3-n */
						b++;
				}
				}
			}
		} else {
			for (int j = n - 1; j > i + 2; j -= 1) {	/* [i+2,n-1)    i+3-n */
				b++;
			} for (int j = i + 1; j < n; j += 1) {	/* [i+1,4) */
				a++;
	}}} for (int i = 1; i < n - 1; i++) {
		c++;
	} printf("%d %d %d\n", a, b, c);
}				/* after jamming *//* lower = i+3 *//* upper = n *//*   intersected  [i+3,n) *//*   left remaining [0,2) *//*   right remaining [0,0) */
