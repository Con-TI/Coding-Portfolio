#ifndef Options06_h
#define Options06_h

#include "BinModel02.h"

class EurOption{
    private:
        int N;
    
    public:
        void SetN(int N_) {N = N_;}
        virtual double Payoff(double z) = 0;
        double PriceByCRR(BinModel Model);
};

class AmOption{
    private:
        int N;
    
    public:
        void SetN(int N_) {N = N_;}
        virtual double Payoff(double z) = 0;
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