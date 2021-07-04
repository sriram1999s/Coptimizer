int main()
{
  int a = 5;
  for( int i = 0; i<40 ; i+=2)
  {
    a+=i; /* ++a ; */
  }

  for( int i = 0; i<41 ; i+=2)
  {
    ++a;
  }
}
