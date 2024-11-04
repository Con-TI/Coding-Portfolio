#include "BSModel02.h"
#include <cmath>
#include <ctime>

const double pi = 4.0*atan(1.0);

double Gauss(){
    double U1 = (rand()+1.0)/(RAND_MAX+1.0);
    double U2 = (rand()+1.0)/(RAND_MAX+1.0);
    return sqrt(-2.0*log(U1))*cos(2.0*pi*U2);
}

Vector Gauss(int d){
    Vector Z(d);
    for (int j=0; j<d; j++) Z[j] = Gauss();
    return Z;
}

// C acts as a matrix that determines the price path by matrix mul
// Interpretation: for every row j in C, the stock price of stock j is determined by the weighted sum of wiener processes
// each wiener process then has a weight corresponding to the row entry in C.
BSModel::BSModel(Vector S0_, double r_, Matrix C_){
    S0 = S0_; r = r_; C = C_; srand(time(NULL));
    //adjusting to num assets
    int d = S0.size();
    sigma.resize(d);
    for (int j=0; j<d; j++) sigma[j] = sqrt(C[j] ^ C[j]);
}

void BSModel::GenerateSamplePath(double T, int m, SamplePath & S){
    Vector St = S0;
    int d = S0.size();
    for (int k=0; k<m; k++){
        S[k] = St*exp((T/m)*(r+(-0.5)*sigma*sigma)+sqrt(T/m)*(C*Gauss(d)));
        St = S[k];
    }
}