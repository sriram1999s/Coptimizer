#include <iostream>
using namespace std;

int main()
{
  long int *a = (long int *)malloc(sizeof(long int) * 1000000000);
  #if 0
  // loop
    for(long int i = 0; i < 1000000000; ++i)
    {
      a[i] = i;
    }

  #endif

  #if 1
  // partial unrolling
    for(long int i = 0; i < 1000000000 - 4; i += 4)
    {
      a[i] = i;
      a[i + 1] = i + 1;
      a[i + 2] = i + 2;
      a[i + 3] = i + 3;
    }


  #endif
}
