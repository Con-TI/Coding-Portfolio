#include "CV.h"
#include "EurCall.h"

double ControlVariate::Payoff(SamplePath & S){
    int d = S[0].size();
    double Sum = 0.0;
    double S_j;
    double K_j;
    double S_sum = 0.0;
    for (int i=0; i<d; i++){
        S_sum += S[0][i];
    }
    for (int i=0; i<d; i++){
        S_j = S[m-1][i];
        K_j = K*S[0][i]/S_sum;
        if (S_j > K_j) S_j = S_j - K_j;
        else S_j = 0.0;
        Sum += S_j;
    }
    return Sum;
}

double ControlVariate::PriceByBSFormula(BSModel Model){
    int d = Model.S0.size();
    double K_j;
    double S_sum = 0.0;
    double Sum = 0.0;
    for (int i=0; i<d; i++){
        S_sum += Model.S0[i];
    }
    for (int i = 0; i<d; i++){
        K_j = K*Model.S0[i]/S_sum;
        EurCall G(T,K_j);
        Sum += G.PriceByBSFormula(Model.S0[i],Model.sigma[i],Model.r);
    }
    Price = Sum;
    return Price;
}