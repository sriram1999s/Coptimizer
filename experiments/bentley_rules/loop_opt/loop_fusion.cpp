#include <iostream>
using namespace std;



int main()
{
  long int count1 = 0;
  long int count2 = 0;
  #if 0
  // seperate loops
    for(long int i = 0; i < 1000000000; i++)
    {
      ++count1;
    }

    for(int j = 0; j < 1000000000; j++)
    {
      ++count2;
    }
  #endif

  #if 1
  // fused loop
    for(long int i = 0; i < 1000000000; i++)
    {
      ++count1;
      ++count2;
    }

  #endif
}
