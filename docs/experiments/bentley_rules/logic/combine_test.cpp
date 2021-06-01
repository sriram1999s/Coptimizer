#include <iostream>
using namespace std;

int main() // full adder
{

  bool a = 1, b = 1, c = 1;
  bool sum, carry;

  #if 0
  // multiple tests
    if(a == 0)// a is 0
    {
      if(b == 0) // b is 0
      {
        if(c == 0)
        {
          sum = 0;
          carry = 0;
        }
        else
        {
          sum = 1;
          carry = 0;
        }
      }
      else // b is 1
      {
        if(c == 0)
        {
          sum = 1;
          carry = 0;
        }
        else
        {
          sum = 0;
          carry = 1;
        }
      }
    }
    else // a is 1
    {
      if(b == 0) // b is 0
      {
        if(c == 0)
        {
          sum = 1;
          carry = 0;
        }
        else
        {
          sum = 0;
          carry = 1;
        }
      }
      else // b is 1
      {
        if(c == 0)
        {
          sum = 0;
          carry = 1;
        }
        else
        {
          sum = 1;
          carry = 1;
        }
      }
    }
  #endif

  #if 1
  // single test
    int res = ((a == 1) << 2 )| ((b == 1) << 1 )| (c == 1);
    switch(res)
    {
      case 0:
        sum = 0;
        carry = 0;
        break;
      case 1:
        sum = 1;
        carry = 0;
        break;
      case 2:
        sum = 1;
        carry = 0;
        break;
      case 3:
        sum = 0;
        carry = 1;
        break;
      case 4:
        sum = 1;
        carry = 0;
        break;
      case 5:
        sum = 0;
        carry = 1;
        break;
      case 6:
        sum = 0;
        carry = 1;
        break;
      case 7:
        sum = 1;
        carry = 1;
        break;
    }
  #endif
    cout << "sum : " << sum << "\ncarry : " << carry << endl;

}
