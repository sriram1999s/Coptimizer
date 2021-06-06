#include<stdio.h>

int main() {
  int n;
  scanf("%d",&n);         /* n = 4 */
  int a=0;
  int b=0;
  int c=0;
  for(int i=0;i<n;i++) {             /* [0,4) */
      for(int j=i+1;j<n;j+=1) {             /* [i+1,4) */
      a++;
    }
    for(int j=n-1;j>i+2;j-=1) {             /* [i+2,n-1)    i+3-n*/
      b++;
    }
  }

  for(int i=1;i<n-1;i++) {
    c++;
  }

  printf("%d %d %d\n",a,b,c);
}

/* after jamming */

/* lower = i+3 */
/* upper = n */

/*   intersected  [i+3,n) */
/*   left remaining [0,2) */
/*   right remaining [0,0) */
  


