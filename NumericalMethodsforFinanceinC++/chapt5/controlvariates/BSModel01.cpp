#include "BSModel01.h"
#include <cmath>

// making pi a constant means no need to recalculate, speeding up code
const double pi=4.0*atan(1.0);

// Box-Muller Method
double Gauss(){
    double U1 = (rand()+1.0)/(RAND_MAX+1.0);
    double U2 = (rand()+1.0)/(RAND_MAX+1.0);
    return sqrt(-2.0*log(U1)) * cos(2.0*pi*U2);
}

// making SamplePath a reference makes it run faster since a new one isn't generated every time.
void BSModel::GenerateSamplePath(double T, int m, SamplePath& S){
    double St = S0;
    for (int k=0; k<m; k++){
        S[k] = St*exp((r-sigma*sigma*0.5)*(T/m)+sigma*sqrt(T/m)*Gauss());
        St = S[k];
    }
}