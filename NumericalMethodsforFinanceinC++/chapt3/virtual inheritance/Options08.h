#ifndef Options06_h
#define Options06_h

#include "BinModel02.h"

class Option{
    private:
        int N;
    public:
        void SetN(int N_) {N=N_;}
        int GetN() {return N;}
        virtual double Payoff (double z) = 0;
};

// By adding virtual for virtual inheritance, such that N does not become two distinct copies in Call. 
// Otherwise, when SetN() is called, Call doesn't know which of the two Ns to choose
class EurOption : public virtual Option{
    public:
        double PriceByCRR(BinModel Model);
};

class AmOption : public virtual Option{
    public:
        double PriceBySnell(BinModel Model);
};

class Call: public EurOption, public AmOption{
    private:
        double K;
    public:
        void SetK(double K_) {K=K_;}
        int GetInputData();
        double Payoff(double z);

};

class Put: public EurOption, public AmOption{
    private:
        double K;
    public:
        void SetK(double K_) {K=K_;}
        int GetInputData();
        double Payoff(double z);
        
};

#endif