#include <iostream>
#include <vector>

using namespace std;

void bubbleSort(vector<double>& v) {
    int n = v.size();     
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (v[j] > v[j + 1])
                swap(v[j], v[j + 1]);
        }
    }
}

int main(){
    vector<double> v = {1,2,4,3,5};
    bubbleSort(v);
    for (auto i: v){
        cout<<i<<",";
    }
}