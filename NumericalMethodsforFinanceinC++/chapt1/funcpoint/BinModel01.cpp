#include "BinModel01.h"
#include <iostream>
#include <cmath>
using namespace std;

/*Calculating risk neutral probability q*/
double RiskNeutralProb(double U, double D, double R){
    return (R-D)/(U-D);
}

/*Calculating S at n = n and i = i*/
double S(double S0, double U, double D, int n, int i){
    return S0*pow(1+U,i)*pow(1+D,n-i);
}

int GetInputData(double& S0, double& U, double& D, double& R){
    /*Console inputs for each var*/
    cout<< "Enter S0: "; cin>>S0;
    cout<< "Enter U: "; cin>>U;
    cout<< "Enter D: "; cin>>D;
    cout<< "Enter R: "; cin>>R;
    
    /*Making sure S0 > 0, -1<R, -1<D<U*/
    if (S0<=0.0 || U<=-1 || D<=-1 || R<=-1 || U<=D){
        cout<< "Illegal Data Ranges" <<endl;
        cout<< "Terminating program" <<endl;
        return 1;
    }
    
    /*Checking for arbitrage*/
    if (R>=U || R<=D){
        cout<< "Arbitrage Exists" <<endl;
        cout<< "Terminating program" <<endl;
        return 1;
    }

    cout << "Input data checked" << endl;
    cout << "No Arbitrage" << endl << endl;

    return 0;
}
