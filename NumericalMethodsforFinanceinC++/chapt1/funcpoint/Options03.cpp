#include "BinModel01.h"
#include "Options03.h"
#include <iostream>
#include <cmath>
using namespace std;

int GetInputData(int& N, double* K[]){
    cout << "Enter steps to expiry N: "; cin >> N;
    for (int i=0; i<2; i++){
        K[i] = new double;
        cout << "Enter strike price K: "; cin >> *K[i];
    }
    cout << endl;
    return 0;
}

double PriceByCRR(double S0, double U, double D, double R, int N, double K[], double (*Payoff) (double z, double K[])){
    double q = RiskNeutralProb(U, D, R);
    double Price[N+1];
    for (int i=0; i<=N; i++){
        Price[i] = Payoff(S(S0,U,D,N,i),K);
    }
    for (int n= N-1; n>=0;n--){
        for (int i=0; i<=n; i++){
            Price[i]= (q*Price[i+1] + (1-q)*Price[i])/(1+R);
        }
    }
    return Price[0];
}

double CallPayoff(double z, double K[]){
    if (z>K[0]) return z-K[0];
    return 0.0;
}

double PutPayoff(double z, double K[]){
    if (z<K[0]) return K[0]-z;
    return 0.0;
}

double DoubleDigPayoff(double z, double K[]){
    if (K[0]<z<K[1]) return 1;
    return 0.0;
}

double DigCallPayoff(double z, double K[]){
    if (z>K[0]) return 1;
    return 0.0;
}

double DigPutPayoff(double z, double K[]){
    if (z<K[0]) return 1;
    return 0.0;
}