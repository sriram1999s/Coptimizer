#include<stdio.h>
int check_overlap(int x1, int y1, int x2, int y2) {if(x1>y1 || x2>y2)return 0;if((x1>=x2 && x1<y2) || (y1>x2 && y1<=y2) || ((x1<y1?x1:y1) > (x2<y2?x2:y2) && (x1>y1?x1:y1) < (x2>y2?x2:y2)) ||((x1<y1?x1:y1) < (x2<y2?x2:y2) && (x1>y1?x1:y1) > (x2>y2?x2:y2)))return 1;return 0;}int main(){int var1=1;int var2;if (var1==0){if (var1==10){int a;}else {int b;}if (var1==0){int c;}else {int d;}}else {int e;}int h;if (var2==1){int f;}else {int g;}return 0;}