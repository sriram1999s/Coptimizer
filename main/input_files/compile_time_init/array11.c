int main() {
    int b[10];
    int a[] = {1,2,3,4};
    int c[2][2];
    int d[10];
    int e[10];
    int k;
    for(int i=0;i<2;i++) {
	for(int j=0;j<2;j++) {
	    for(int k=0;k<3;++k) {
		b[j] = i;
	    }
	}
    }

    for(int i=0;i<5;i++) {
	d[i] = 0;
    }

    for(int i=0;i<5;i++) {
	e[i] = 0;
    }
}
