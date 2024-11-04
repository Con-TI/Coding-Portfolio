#ifndef RegEurCall_h
#define RegEurCall_h

#include "PathDepOption04.h"

class RegEurCall : public PathDepOption{
    public: 
        double K;
        RegEurCall(double T_, double K_, double m_){ 
            T = T_; K = K_; m = m_;
        }
        double Payoff(SamplePath& S);
        double PriceByBSFormula(BSModel Model);
};

#endif