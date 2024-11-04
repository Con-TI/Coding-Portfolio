#ifndef Options05_h
#define Options05_h

#include "BinModel02.h"

class EurOption{
    private:
        int N;
        double (*Payoff) (double z, double K);
    public:
        void SetN(int N_){
            N=N_;
        }
        void SetPayoff(double (*Payoff_) (double z, double K)){
            Payoff = Payoff_;
        }
        double PriceByCRR(BinModel Model, double K);
};

double CallPayoff(double z, double K);


// Makes a subclass Call of EurOption which puts all public members of EurOption as public members of itself.
class Call: public EurOption{
    private:
        double K;
    public:
        // Constructor function. It is executed automatically when object is initialized.
        Call(){
            SetPayoff(CallPayoff);
        }
        double GetK(){
            return K;
        };
        int GetInputData();
};

double PutPayoff(double z, double K);

class Put: public EurOption{
    private:
        double K;
    public:
        Put(){
            SetPayoff(PutPayoff);
        }
        double GetK(){
            return K;
        };
        int GetInputData();
};

#endif