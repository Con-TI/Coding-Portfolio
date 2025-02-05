#ifndef PathDepOption02_h
#define PathDepOption02_h

#include "BSModel01.h"

class PathDepOption{
    public:
        double T,Price, PricingError;  
        int m;
        double PriceByMC(BSModel Model, long N);
        virtual double Payoff(SamplePath& S) = 0;
};

class ArthmAsianCall: public PathDepOption{
    public:
        double K;
        ArthmAsianCall(double T_, double K_, int m_) {T=T_; K=K_; m=m_;}
        double Payoff(SamplePath& S);
};

#endif