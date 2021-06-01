#include<stdio.h>
int check_overlap(int x1, int y1, int x2, int y2)
{
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
	int a = 0;
	int b = 0;
	scanf("%d", &n);
	if (check_overlap(1, n, 3, n + 3)) {
		int temp_1624b40f734a = 1;
		int temp_eb30c81630c2 = (n < n + 3 ? n : n + 3);
		int temp_037ad97296a7 = 3;
		int temp_282dbdb736ee = (n > n + 3 ? n : n + 3);
		for (int i = temp_037ad97296a7; i < temp_eb30c81630c2; ++i) { {
				++a;
		} {
			++b;
		}} for (int i = 0; i < (temp_037ad97296a7 - temp_1624b40f734a);
			++i) {
			if (temp_1624b40f734a == 3) { {
					++a;
			}
			} else { {
					++b;
			}
			}
		}
		for (int z = 0; z < (temp_282dbdb736ee - temp_eb30c81630c2);
		     z++) {
			if (temp_282dbdb736ee == n + 3) { {
					++a;
			}
			} else { {
					++b;
			}
			}
		}
	} else {
		for (int i = 1; i < n; ++i) {
			++b;
		} for (int i = 3; i < n + 3; ++i) {
			++a;
	}} printf("a : %d, b : %d", a, b);
}
