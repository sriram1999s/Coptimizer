#include <iostream>
using namespace std;

int main()
{

  int a[51]  = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49};


  #if 0
  // linear search
    int i = 0;
    while(i < 50) // to find number 101
    {
        if(i == 101)
        {
          cout << "101 is found at :" << i << '\n';
          return 0;
        }
        ++i;
    }
    cout << "101 not found \n";

  #endif

  #if 1
  // sentinel linear search
    int i = 0;
    a[50] = 101;
    while(i != 101)
    ++i;

    if(i < 50)
    cout << "101 is found at :" << i << '\n';
    else
    cout << "101 not found \n";

  #endif
}
