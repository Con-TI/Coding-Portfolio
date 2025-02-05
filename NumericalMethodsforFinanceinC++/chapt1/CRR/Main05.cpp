#include "Options01.h"
#include "BinModel01.h"
#include <iostream>
#include <cmath>
using namespace std;

int main(){
    double S0, U, D, R;

    if (GetInputData(S0, U, D, R)==1) return 1;

    double K;
    int N;

    cout << "Enter call option data: "<<endl;
    GetInputData(N, K);
    cout << "European call option price = " 
    << PriceByCRR(S0, U, D, R, N, K)
    << endl << endl;

    char x; cin >> x;

    return 0;

}