#ifndef Options01_h
#define Options01_h

int GetInputData(int& N, double* K[]);

double PriceByCRR(double S0, double U, double D, double R, int N, double K[], double (*Payoff) (double z, double K[]));

double CallPayoff(double z, double K[]);

double PutPayoff(double z, double K[]);

double DigCallPayoff(double z, double K[]);

double DigPutPayoff(double z, double K[]);

double DoubleDigPayoff(double z, double K[]);

#endif