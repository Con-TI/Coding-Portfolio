#include <iostream>
#include "PathDepOption04.h"
#include "GmtrAsianCall.h"
#include "RegEurCall.h"

using namespace std;

int main(){
    double S0 = 100.0, r =0.03, sigma=0.2;
    BSModel Model(S0, r, sigma);
    double T= 1.0/12.0, K=100.0;
    int m=30;
    ArthmAsianCall Option(T,K,m);
    GmtrAsianCall CVOption(T,K,m);

    long N = 30000;
    Option.PriceByVarRedMC(Model, N, CVOption);
    cout << "Arithmetic call price = " << Option.Price << endl 
    << "Error = " << Option.PricingError << endl    
    << "Delta = " << Option.delta << endl;
    Option.PriceByMC(Model, N);
    cout << "Price by direct MC = " << Option.Price << endl 
    << "MC Error = " << Option.PricingError << endl
    << "Delta = " << Option.delta << endl << endl;

    double L = 120;
    BarrCall Option2(T,K,m,L);
    RegEurCall CVOption2(T,K,m);
    Option2.PriceByVarRedMC(Model, N, CVOption2);
    cout << "Barrier call price = " << Option2.Price << endl
    << "Error = " << Option2.PricingError << endl
    << "Delta = " << Option2.delta << endl;
    Option2.PriceByMC(Model, N);
    cout << "Price by direct MC = " << Option2.Price << endl 
    << "MC Error = " << Option2.PricingError << endl
    << "Delta = " << Option2.delta << endl;
    
    char x; cin >> x;
    return 0;
}