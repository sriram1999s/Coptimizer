#include <iostream>
using namespace std;

int main()
{
  int a[30];
  #if 0
  // loop
    for(long int i = 0; i < 30; i++)
    {
      a[i] = i;
    }

  #endif

  #if 1
  // unrolled loop

    a[0] = 0;
    a[1] = 1;
    a[2] = 2;
    a[3] = 3;
    a[4] = 4;
    a[5] = 5;
    a[6] = 6;
    a[7] = 7;
    a[8] = 8;
    a[9] = 9;
    a[10] = 10;
    a[11] = 11;
    a[12] = 12;
    a[13] = 13;
    a[14] = 14;
    a[15] = 15;
    a[16] = 16;
    a[17] = 17;
    a[18] = 18;
    a[19] = 19;
    a[20] = 20;
    a[21] = 21;
    a[22] = 22;
    a[23] = 23;
    a[24] = 24;
    a[25] = 25;
    a[26] = 26;
    a[27] = 27;
    a[28] = 28;
    a[29] = 29;

  #endif
}
