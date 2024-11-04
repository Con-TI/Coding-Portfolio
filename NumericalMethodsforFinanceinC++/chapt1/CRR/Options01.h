#ifndef Options01_h
#define Options01_h

int GetInputData(int& N, double&K);

double PriceByCRR(double S0, double U, double D, double R, int N, double K);

double CallPayoff(double z, double K);

#endif