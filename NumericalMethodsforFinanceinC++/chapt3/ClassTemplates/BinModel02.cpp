#include "BinModel02.h"
#include <iostream>
#include <cmath>
using namespace std;

double BinModel::RiskNeutProb(){
    return (R-D)/(U-D);
}
double BinModel::S(int n, int i){
    return S0*pow(1+U,i)*pow(1+D,n-i);
}

/*Exercise 3.2*/
// int BinModel::GetInputData(){
//     cout << "Enter S0: "; cin >> S0;
//     double T;
//     int N;
//     double r;
//     double sigma;
//     cout << "Enter total time T: "; cin >> T;
//     cout << "Enter steps N: "; cin >> N;
//     cout << "Enter continuously compounded rate r: "; cin >> r;
//     cout << "Enter volatility sigma"; cin >> sigma;
//     double h = T/N;

//     U = exp((r+pow(sigma,2)/2)*h + sigma*sqrt(h))-1;
//     D = exp((r+pow(sigma,2)/2)*h - sigma*sqrt(h))-1;
//     R = exp(r*h)-1;

//     if (S0 <= 0 || U <= -1.0 || D <= -1.0 || U<=D || R<=-1.0){
//         cout << "Illegal data ranges" << endl;
//         cout << "Terminating program" << endl;
//         return 1;
//     }
//     if (R>=U || R <= D){
//         cout << "Arbitrage exitsts" << endl;
//         cout << "Terminating program" << endl;
//         return 1;
//     }

//     cout << "Input data checked" << endl;
//     cout << "There is no arbitrage" << endl << endl;

//     return 0;
// }

int BinModel::GetInputData(){
    cout << "Enter S0: "; cin >> S0;
    cout << "Enter U: "; cin >> U;
    cout << "Enter D: "; cin >> D;
    cout << "Enter R: "; cin >> R;
    cout << endl;
    if (S0 <= 0 || U <= -1.0 || D <= -1.0 || U<=D || R<=-1.0){
        cout << "Illegal data ranges" << endl;
        cout << "Terminating program" << endl;
        return 1;
    }
    if (R>=U || R <= D){
        cout << "Arbitrage exitsts" << endl;
        cout << "Terminating program" << endl;
        return 1;
    }

    cout << "Input data checked" << endl;
    cout << "There is no arbitrage" << endl << endl;

    return 0;
}

double BinModel::GetR(){
    return R;
}