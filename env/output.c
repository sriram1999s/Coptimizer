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
	scanf("%d", &n);
	int a = 0;
	int b = 0;
	int k = 3;
	if (check_overlap(4 + 1, n - 1 + 1, 3, n)) {
		int temp_4e56e2063c2d = 3;
		int temp_2898847f7acd = (n - 1 + 1 < n ? n - 1 + 1 : n);
		int temp_128e7a861a68 = 5;
		int temp_dfeddef4ab93 = (n - 1 + 1 > n ? n - 1 + 1 : n);
		for (int j = temp_128e7a861a68; j < temp_2898847f7acd; j += 1) { {
				a++;
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
				a = a * 2 + a - 3 + (1000);
		} {
			b++;
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
		}} for (int j = 0; j < (temp_128e7a861a68 - temp_4e56e2063c2d);
			j += 1) {
			if (temp_4e56e2063c2d == 3) { {
					a++;
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
			}
			} else { {
					b++;
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
			}
			}
		}
		for (int z = 0; z < (temp_dfeddef4ab93 - temp_2898847f7acd);
		     z++) {
			if (temp_dfeddef4ab93 == n) { {
					a++;
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
					a = a * 2 + a - 3 + (1000);
			}
			} else { {
					b++;
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
					b = b * 2 + b - 3 + (1000);
			}
			}
		}
	} else {
		for (int j = n - 1; j > 4; j -= 1) {
			b++;
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
			b = b * 2 + b - 3 + (1000);
		} for (int j = 3; j < n; j += 1) {
			a++;
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
			a = a * 2 + a - 3 + (1000);
	}} printf("%d %d\n", a, b);
}
