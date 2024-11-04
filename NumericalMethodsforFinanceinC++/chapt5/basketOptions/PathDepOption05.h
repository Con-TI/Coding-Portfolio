#ifndef PathDepOption05_h
#define PathDepOption05_h

#include "BSMOdel02.h"

class PathDepOption{
    public:
        double T;
        int m;
        double Price;
        double PricingError;
        Vector Delta;
        double PriceByMC(BSModel Model, long N, double epsilon);
        double PriceByVarRedMC(BSModel Model, long N, PathDepOption& CVOption, double epsilon);
        virtual double Payoff(SamplePath & S) = 0;
        virtual double PriceByBSFormula(BSModel Model) {return 0.0;}
};

class ArthmAsianCall: public PathDepOption{
    public:
        double K;
        ArthmAsianCall(double T_, double K_, int m_){
            T=T_; K=K_; m=m_;
        }
        double Payoff(SamplePath & S);
};

class EurBasketCall: public PathDepOption{
    public: 
        double K;
        EurBasketCall(double T_, double K_, int m_){
            T=T_; K=K_; m=m_;
        }
        double Payoff(SamplePath& S);
};

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

#endif 