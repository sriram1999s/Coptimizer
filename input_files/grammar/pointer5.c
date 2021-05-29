int foo(int *, int);
int bar(int *a, int *b);
int cat(int x, int *y);
int main()
{
  int a;
  int *p;
  int *q = &a;
  p = q;
}
