#include<stdio.h>
#include<time.h>
int main() {
    int a=0;
    int n;
    scanf("%d",&n);
    double startTime = (float)clock()/CLOCKS_PER_SEC;
    for(int i=0;i<n;i++) {
	a++;
    }
    double endTime = (float)clock()/CLOCKS_PER_SEC;
    double timeElapsed = endTime - startTime;
    printf("%d\n", a);
    printf("%lf\n",timeElapsed);
}
	
