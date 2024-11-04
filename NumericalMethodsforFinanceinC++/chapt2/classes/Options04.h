#ifndef Options04_h
#define Options04_h

#include "BinModel02.h"

int GetInputData(int & N, double & K);
// Object BinModel is passed into function
double PriceByCRR(BinModel Model, int N, double K, double (*Payoff) (double z, double k));
double CallPayoff(double z, double K);
double PutPayoff(double z, double K);

#endif