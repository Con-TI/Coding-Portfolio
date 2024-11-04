#ifndef PathDepOption04_h
#define PathDepOption04_h

#include "BSModel01.h"

class PathDepOption{
    public:
        double T, Price, PricingError, delta;
        int m;
        virtual double Payoff(SamplePath& S)=0;
        double PriceByMC(BSModel Model, long N);
        // CV Option is the control variate. Pricing function using control variate.
        double PriceByVarRedMC(BSModel Model, long N, PathDepOption& CVOption);
        // Analytic formula for control variate.
        virtual double PriceByBSFormula(BSModel Model) {return 0.0;}
};

// Create class that returns difference in payoffs
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

class ArthmAsianCall:public PathDepOption{
    public:
        double K;
        ArthmAsianCall(double T_, double K_, int m_){
            T = T_; K = K_; m = m_;
        }
        double Payoff(SamplePath& S);
        double Delta();
};

class BarrCall: public PathDepOption{
    public: 
        double K;
        double L;
        BarrCall(double T_, double K_, double m_, double L_){ 
            T = T_; K = K_; m = m_; L = L_;
        }
        double Payoff(SamplePath& S);
};

#endif