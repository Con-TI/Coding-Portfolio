#ifndef Options02_h
#define Options02_h

int GetInputData(int* PtrN, double* PtrK);

double PriceByCRR(double S0, double U, double D, double R, int N, double K);

double CallPayoff(double z, double K);

#endif