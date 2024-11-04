#include <iostream>
#include "PathDepOption05.h"
#include "CV.h"

using namespace std;

int main(){
    int d=3;
    Vector S0(d);
        S0[0] = 40.0;
        S0[1] = 60.0;
        S0[2] = 100.0;
    double r = 0.03;
    Matrix C(d, Vector(d));    
        C[0][0] = 0.1; C[0][1] = -0.1; C[0][2] = 0.0;
        C[1][0] = -0.1; C[1][1] = 0.2; C[1][2] = 0.0;
        C[2][0] = 0.0; C[2][1] = 0.0; C[2][2] = 0.3;
    BSModel Model(S0, r, C);
    double T=1.0/12.0, K=200.0;
    int m=30;
    ArthmAsianCall Option(T,K,m);

    long N=30000;
    double epsilon = 1e-5;
    Option.PriceByMC(Model, N, epsilon);
    cout << "Arithmetic Basket Call Price = "
    << Option.Price << endl
    << "Price Error = "
    << Option.PricingError << endl;
    for (int i = 0; i<d; i++){
        cout << "Delta " << i << " = "
        << Option.Delta[i] << endl;
    }

    EurBasketCall Option2(T,K,m);
    Option2.PriceByMC(Model,N,epsilon);
    cout << "European Basket Call Price = "
    << Option2.Price << endl
    << "Price Error = "
    << Option2.PricingError << endl;
    for (int i = 0; i<d; i++){
        cout << "Delta " << i << " = "
        << Option2.Delta[i] << endl;
    }

    ControlVariate CVOption(T, K, m);
    Option2.PriceByVarRedMC(Model, N, CVOption, epsilon);
    cout << "European Basket Call Price = "
    << Option2.Price << endl
    << "Price Error = "
    << Option2.PricingError << endl;
    
    char x; cin >> x;
    return 0;
}