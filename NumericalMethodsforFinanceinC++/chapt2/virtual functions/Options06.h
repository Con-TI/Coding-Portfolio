#ifndef Options06_h
#define Options06_h

#include "BinModel02.h"

// Called an abstract class since it has a pure (i.e. = 0) virtual function
class EurOption{
    private:
        int N;
    
    public:
        void SetN(int N_) {N = N_;}
        // Being declared virtual makes the version of Payoff() belonging to that subclass get executed.
        // having = 0 makes compiler know there is no definition here.
        virtual double Payoff(double z) = 0;
        // virtual double Payoff(double z) {return 0.0;}
        double PriceByCRR(BinModel Model);
};

class Call: public EurOption{
    private:
        double K;
    public:
        void SetK(double K_) {K=K_;}
        int GetInputData();
        double Payoff(double z);

};

class Put: public EurOption{
    private:
        double K;
    public:
        void SetK(double K_) {K=K_;}
        int GetInputData();
        double Payoff(double z);
        
};

class BullSpread: public EurOption{
    private:
        double K1;
        double K2;
    public:
        void SetK(double K1_, double K2_) {K1=K1_;K2=K2_;}
        int GetInputData();
        double Payoff(double z);
};

class BearSpread: public EurOption{
    private:
        double K1;
        double K2;
    public:
        void SetK(double K1_, double K2_) {K1=K1_;K2=K2_;}
        int GetInputData();
        double Payoff(double z);
};

class Strangle: public EurOption{
    private:
        double K1;
        double K2;
    public:
        void SetK(double K1_, double K2_) {K1=K1_;K2=K2_;}
        int GetInputData();
        double Payoff(double z);
};

class Butterfly: public EurOption{
    private:
        double K1;
        double K2;
    public:
        void SetK(double K1_, double K2_) {K1=K1_;K2=K2_;}
        int GetInputData();
        double Payoff(double z);
};


#endif