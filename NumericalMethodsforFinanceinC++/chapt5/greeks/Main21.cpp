#include <iostream>
#include "PathDepOption03.h"

using namespace std;

int main(){
    double S0 = 100, r = 0.03, sigma = 0.2;
    BSModel Model(S0, r, sigma);
    double T = 1.0/12.0, K = 100.0;
    int m = 30;
    ArthmAsianCall Option(T,K,m);

    long N = 30000;
    double epsilon = 1e-4;
    cout << "Asian Call Price = "
    << Option.PriceByMC(Model, N, epsilon) << endl
    << "Pricing Error = " 
    << Option.PricingError <<  endl
    << "Delta = "
    << Option.delta << endl
    << "Gamma = "
    << Option.gamma << endl
    << "Vega = "
    << Option.vega << endl
    << "Theta = "
    << Option.theta << endl
    << "Rho = "
    << Option.rho << endl;

    char x; cin >> x;

    return 0;
}