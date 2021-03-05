int foo(int *, int);
int bar(int *a, int *b);
int cat(int x, int *y);
int main()
{
  int *p, a;
  a = 10;
  p = &a;
  foo(p,a);
}
