#include<stdio.h>
int fooq(int m,int n);
int foo()
{
  int x = 10;
  return x;
}
char foox(int x, float b)
{
  char ch = 97;
  return ch;
}
int foop(int a, int b, int c)
{
  int res = a*b-c;
  return foox(foo(),fooq(foo(),fooq(foo(),foo())));
}
int fooq(int m,int n)
{
  return m + n;
}
int main()
{
  int a;
  int b;
  scanf("%d %d",&a,&b);
  printf("a : %d b : %d\n",a,b);
  scanf("%d",&a);
  printf("Hello world!\n");
  printf("%s\n","YO");
  printf("%d\n",printf("A"));
  foo();
  foo1();
  foo2();
  foo3();
  printf("%d %d %c\n",foo(),foo(),foox(10,20));
  char ch = foox(foox(foo(),19),foo()) ;
  char ch1;
  ch1 = foox(foox(foo(),19),foo());
  ch1 = foox(10,20);
  foop(1,2,3);
  return 0;
}
