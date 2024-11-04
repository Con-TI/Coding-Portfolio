#ifndef BinModel01_h
#define BinModel01_h

/*Calculating risk neutral probability q*/
double RiskNeutralProb(double U, double D, double R);

/*Calculating S at n = n and i = i*/
double S(double S0, double U, double D, int n, int i);

int GetInputData(double *S0, double *U, double *D, double *R);


#endif