int main()
{
  int a;
  int b = 10;
  {
    int a;
    a = b;
  }
  b = 12;
  a = 15;
}
