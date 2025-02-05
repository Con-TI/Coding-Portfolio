#ifndef PathDepOption01_h
#define PathDepOption01_h

#include "BSModel01.h"

class PathDepOption{
    public:
        // double T refers to total time in yrs
        // int m refers time steps
        double T;
        int m;
        // Number of sample paths N
        double PriceByMC(BSModel Model, long N);
        virtual double Payoff(SamplePath& S) = 0;
};

class ArthmAsianCall: public PathDepOption{
    public:
        // double K is strike price
        double K;
        ArthmAsianCall(double T_, double K_, int m_){
            T=T_; K=K_; m=m_;
        }
        double Payoff(SamplePath& S);
};

class EurCall: public PathDepOption{
    public:
        double K;
        EurCall(double T_, double K_, int m_){
            T = T_; K=K_; m=m_;
        }
        double Payoff(SamplePath& S);
};


class EurPut: public PathDepOption{
    public:
        double K;
        EurPut(double T_, double K_, int m_){
            T = T_; K=K_; m=m_;
        }
        double Payoff(SamplePath& S);
};

#endif 