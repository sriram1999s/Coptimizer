int main() {
    int a,b,c;
    a=1*2;
    b=a;
    c=a;
    {
	int d=a;
    }
    a=7;
    b=a;
}
