int main()
{
  int a = 5;
  for( int i = 1; i< 68719476736 ; i*=2)
  {
    ++a;
  }
  for( int i = 1; i< 68719476737 ; i*=2)
  {
    ++a;
  }
}
