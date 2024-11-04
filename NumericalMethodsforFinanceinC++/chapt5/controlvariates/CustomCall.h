#ifndef CustomCall_h
#define CustomCall_h

#include "PathDepOption04.h"

class CustomCall: public PathDepOption{
    public: 
        double K;
        CustomCall(double T_, double K_, double m_){ 
            T = T_; K = K_; m = m_;
        }
        double Payoff(SamplePath& S);
        double PriceByBSFormula(BSModel Model);
};


#endif