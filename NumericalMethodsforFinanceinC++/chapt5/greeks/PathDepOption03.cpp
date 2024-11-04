#include "PathDepOption03.h"
#include <cmath>

// Multiplies sample path by number. For the (1+epsilon)S
void Rescale(SamplePath& S, double x){
    int m=S.size();
    for (int j=0; j<m; j++) S[j] = x*S[j];
}

// delta, the rate of change in option price per unit change in underlying
// estimation based off of derivative approaching linear at small epsilon.
// Using finite difference methods to form these estimations
// For theta, it would be (V(T-deltaT)-V(T))/delta T, where T is time to maturity
double PathDepOption::PriceByMC(BSModel Model, long N, double epsilon){
    double H=0.0, Hsq=0.0, Heps=0.0, Heps2=0.0, Hthet = 0.0, Hveg = 0.0, Hr = 0.0;
    SamplePath S(m);
    BSModel Model2(Model.S0, Model.r, Model.sigma*(1+epsilon));
    BSModel Model3(Model.S0, Model.r*(1+epsilon), Model.sigma);
    for (long i=0; i<N; i++){
        Model.GenerateSamplePath(T,m,S);
        H = (i*H + Payoff(S))/(i+1.0);
        Hsq = (i*Hsq + pow(Payoff(S),2.0))/(i+1.0);
        Rescale(S, 1.0+epsilon);
        Heps = (i*Heps + Payoff(S))/(i+1.0);
        Rescale(S, (1.0-epsilon)/(1.0+epsilon));
        Heps2 = (i*Heps2 + Payoff(S))/(i+1.0);

        Model.GenerateSamplePath(T*(1-epsilon),m,S);
        Hthet = (i*Hthet + Payoff(S))/(i+1.0);

        Model2.GenerateSamplePath(T,m,S);
        Hveg = (i*Hveg + Payoff(S))/(i+1.0);

        Model3.GenerateSamplePath(T,m,S);
        Hr = (i*Hr + Payoff(S))/(i+1.0);
    }
    Price = exp(-Model.r*T)*H;
    PricingError = exp(-Model.r*T)*sqrt(Hsq-H*H)/sqrt(N-1.0);
    delta = exp(-Model.r*T)*(Heps-H)/(Model.S0*epsilon);
    gamma = exp(-Model.r*T)*(Heps + Heps2 - 2*H)/pow((Model.S0*epsilon),2);
    theta = exp(-Model.r*T)*(Hthet - H)/(-T*epsilon);
    vega = exp(-Model.r*T)*(Hveg - H)/(Model.sigma*epsilon);
    rho = exp(-Model.r*T)*(Hr - H)/(Model.r*epsilon);
    return Price;
}

double ArthmAsianCall::Payoff(SamplePath& S){
    double Ave=0.0;
    for (int k=0; k<m; k++) Ave=(k*Ave + S[k])/(k+1.0);
    if (Ave<K) return 0;
    return Ave-K;
}