#include<stdio.h>
#include<stdlib.h>

int main() {
    int n;
    int s;
    scanf("%d %d",&n,&s);
    int* a = malloc(sizeof(int)*n);
    for(int i=0;i<n;i++) {
	scanf("%d",&a[i]);
    }

    int c_j = 0;
    for(int j=0;j<n;++j) {
	if(a[c_j]==s) {
	    printf("found: %d\n",c_j);
	}
	++c_j;
    }
    printf("scene illa guru!!\n");
}
    
