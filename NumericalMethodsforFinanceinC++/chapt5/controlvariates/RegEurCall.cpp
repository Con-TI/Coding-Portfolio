#include "RegEurCall.h"
#include "EurCall.h"

double RegEurCall::Payoff(SamplePath & S){
    if (S[m-1]>K) return S[m-1]-K;
    return 0;
}

double RegEurCall::PriceByBSFormula(BSModel Model){
    EurCall G(T,K);
    Price = G.PriceByBSFormula(Model.S0, Model.sigma, Model.r);
    delta = G.DeltaByBSFormula(Model.S0, Model.sigma, Model.r, Model.S0);
    return Price;
}