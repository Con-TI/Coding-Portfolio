#include <iostream>
#include "BinModel01.h"
#include <cmath>
using namespace std;

int main(){
    /*Declaring double type of 
    spot price(S0), U, D, R*/
    double S0, U, D, R;
    
    if (GetInputs(S0, U, D, R) == 1) return 1;

    /*Risk neutral probability*/
    cout << "q = " << RiskNeutralProb(U, D, R) << endl;
    
    int n, i;
    cout<< "n = "; cin>> n;
    cout<< "i = "; cin>> i;
    cout<< "S(n,i) = " <<S(S0,U,D,n,i)<<endl;


    char x; cin >> x;
    return 0;
}