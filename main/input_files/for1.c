
int main()
{
  int a = 5;
  for( int i = 0; i< 5;i++)
  {
    ++a;
    int a = 0;
    {
      int a = 3;
    }
  }
}
