#include "PathDepOption04.h"
#include <cmath>
#include <iostream>
using namespace std;

void Rescale(SamplePath& S, double x){
    int m=S.size();
    for (int j=0; j<m; j++) S[j] = x*S[j];
}

double PathDepOption::PriceByMC(BSModel Model, long N){
    double H = 0.0, Hsq = 0.0, Heps = 0.0;
    double epsilon = 0.001;
    SamplePath S(m);
    for (long i=0; i<N; i++){
        Model.GenerateSamplePath(T,m,S);
        H = (i*H + Payoff(S))/(i+1.0);
        Hsq = (i*Hsq + pow(Payoff(S),2.0))/(i+1.0);
        Rescale(S, 1.0+epsilon);
        Heps = (i*Heps + Payoff(S))/(i+1.0);
    }
    Price = exp(-Model.r*T)*H;
    PricingError = exp(-Model.r*T)*sqrt(Hsq-H*H)/sqrt(N-1.0);
    delta = exp(-Model.r*T)*(Heps-H)/(Model.S0*epsilon);
    return Price;
}

double PathDepOption::PriceByVarRedMC(BSModel Model, long N, PathDepOption& CVOption){
    // "this" keyword designates a pointer towards "this" object (if its inside the class, then say ArthmAsianCall c, this points to c.)
    DifferenceOfOptions VarRedOpt(T, m, this, &CVOption);
    Price = VarRedOpt.PriceByMC(Model, N) + CVOption.PriceByBSFormula(Model);
    // Pricing error only comes from H(T)-G(T) since G(0) is calc analytically (so no errors).
    PricingError = VarRedOpt.PricingError;
    delta = VarRedOpt.delta + CVOption.delta;
    return Price;
}

double ArthmAsianCall::Payoff(SamplePath& S){
    double Ave = 0.0;
    for (int k=0; k<m; k++) Ave = (k*Ave+S[k])/(k+1.0);
    if (Ave<K) return 0.0;
    return Ave-K;
}

double BarrCall::Payoff(SamplePath& S){
    double max_S = 0.0;
    for (int i=0; i<m; i++) if (S[i]>max_S) {max_S = S[i];}
    if (max_S > L) return 0.0;
    else{ 
        if (S[m-1]>K) return S[m-1]-K;
        return 0.0;
    }
}

class DifferenceOfOptions: public PathDepOption{
    public:
        // Pointers to each option
        PathDepOption* Ptr1;
        PathDepOption* Ptr2;
        DifferenceOfOptions (double T_, int m_, PathDepOption* Ptr1_, PathDepOption* Ptr2_){
            T = T_; m = m_; Ptr1 = Ptr1_; Ptr2 = Ptr2_;
        }
        double Payoff(SamplePath& S){
            return Ptr1->Payoff(S) - Ptr2->Payoff(S);
        }
};