#include "PathDepOption05.h"
#include <cmath>
#include <iostream>

using namespace std;

void Rescale(SamplePath & S, int j, double scale){
    int m = S.size();
    for (int i = 0; i<m; i++){
        S[i][j] = scale*S[i][j];
    }
}

double PathDepOption::PriceByVarRedMC(BSModel Model, long N, PathDepOption & CVOption, double epsilon){
    DifferenceOfOptions VarRedOpt(T, m, this, &CVOption);
    Price = VarRedOpt.PriceByMC(Model, N, epsilon) + CVOption.PriceByBSFormula(Model);
    PricingError = VarRedOpt.PricingError;
    return Price;
}

double PathDepOption::PriceByMC(BSModel Model, long N, double epsilon){
    double H = 0.0;
    double Hsq = 0.0;
    Vector Heps(3);
    Heps = {0.0, 0.0, 0.0};
    int d = Model.S0.size();
    SamplePath S(m);
    for (long i =0; i<N; i++){
        Model.GenerateSamplePath(T,m,S);
        H = (i*H + Payoff(S))/(i+1.0);
        Hsq = (i*Hsq + pow(Payoff(S),2))/(i+1.0);
        for (int j = 0; j<d; j++){
            Rescale(S, j, (1+epsilon));
            Heps[j] = (i*Heps[j] + Payoff(S))/(i+1.0);
            Rescale(S, j, (1/(1+epsilon)));
        }
    }
    Price = exp(-Model.r*T)*H; 
    PricingError = exp(-Model.r*T)*sqrt(Hsq-H*H)/sqrt(N-1);
    Delta = exp(-Model.r*T)*(-H+Heps)/(epsilon*Model.S0);
    return Price;
}

// Computing sum of arithmetic averages of each stock.
double ArthmAsianCall::Payoff(SamplePath & S){
    double Ave = 0.0;
    int d=S[0].size();
    Vector one(d);
    for (int i=0; i<d; i++) one[i] = 1.0;
    for (int k=0; k<m; k++){
        Ave = (k*Ave + (one^S[k]))/(k+1.0);
    }
    if (Ave<K) return 0.0;
    return Ave-K;
}

double EurBasketCall::Payoff(SamplePath & S){
    int d=S[0].size();
    Vector one(d);
    for (int i=0; i<d; i++) one[i] = 1.0;
    double Price = one^S[m-1];
    if (Price>K) return Price-K;
    return 0.0;
}