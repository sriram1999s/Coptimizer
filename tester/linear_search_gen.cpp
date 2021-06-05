#include<iostream>
using namespace std;
#include<vector>

int main() {
    int n = 100000000;
    vector<int> a(n);
    for(int i=0;i<n;++i) {
	a[i] = i;
    }
    cout<<n<<" "<<n;
    for(int i=0;i<n;i++) {
	cout<<a[i]<<" ";
    }
    cout<<"\n";
}

    
