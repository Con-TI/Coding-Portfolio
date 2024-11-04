#include "PathDepOption01.h"
#include <cmath>

double PathDepOption::PriceByMC(BSModel Model , long N){
    double H = 0.0;
    //Creates vector<double> with m entries
    SamplePath S(m);
    //Arithmean expected val
    for (long i=0; i<N; i++){
        Model.GenerateSamplePath(T,m,S);
        H = (i*H + Payoff(S))/(i+1.0);
    }
    //Discounted expected value
    return exp(-Model.r*T)*H;
}

double ArthmAsianCall::Payoff(SamplePath& S){
    double Ave = 0.0;
    for (int k=0; k<m; k++) Ave = (k*Ave + S[k])/(k+1.0);
    if (Ave<K) return 0;
    return Ave-K;
}

double EurCall::Payoff(SamplePath& S){
    double S_T = S[-1];
    if (S_T < K) return 0;
    return S_T-K;
}

double EurPut::Payoff(SamplePath& S){
    double S_T = S[-1];
    if (S_T > K) return 0;
    return K-S_T;
}