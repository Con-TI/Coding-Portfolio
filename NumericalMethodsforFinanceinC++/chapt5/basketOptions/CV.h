#ifndef CV_h
#define CV_h

#include "PathDepOption05.h"

class ControlVariate: public PathDepOption{
    public:
        double K;
        ControlVariate(double T_, double K_, double m_){
            T=T_; K=K_; m=m_;
        }
        double Payoff(SamplePath & S);
        double PriceByBSFormula(BSModel Model);
};

#endif