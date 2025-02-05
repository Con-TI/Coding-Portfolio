#include "Options06.h"
#include "BinModel02.h"
#include <iostream>
#include <cmath>
using namespace std;

double EurOption::PriceByCRR(BinModel Model){
    double q = Model.RiskNeutProb();
    double Price[N+1];
    for (int i=0; i<= N; i++){
        Price[i] = Payoff(Model.S(N,i));
    }
    for (int n=N-1; n>=0; n--){
        for (int i=0; i<=n; i++){
            Price[i] = (q*Price[i+1]+(1-q)*Price[i])/(1+Model.GetR());
        }
    }
    return Price[0];
}

int Call::GetInputData()
{
    cout << "Enter call option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K: "; cin >>K;
    cout << endl;
    return 0;
}

double Call::Payoff(double z){
    if (z>K) return z-K;
    return 0.0;
}

int Put::GetInputData()
{
    cout << "Enter call option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K: "; cin >>K;
    cout << endl;
    return 0;
}

double Put::Payoff(double z){
    if (z<K) return K-z;
    return 0.0;
}

double BullSpread::Payoff(double z)
{
    if (K1<z<K2) return z-K1;
    else if(z>K2) return K2-K1;
    return 0.0;
}

int BullSpread::GetInputData(){
    {
    cout << "Enter BullSpread option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K1: "; cin >>K1;
    cout << "Enter strike price K2: "; cin >>K2;
    cout << endl;
    return 0;
}
}

double BearSpread::Payoff(double z)
{
    if (K1<z<K2) return K2-z;
    else if(z<K1) return K2-K1;
    return 0.0;
}

int BearSpread::GetInputData(){
    {
    cout << "Enter BearSpread option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K1: "; cin >>K1;
    cout << "Enter strike price K2: "; cin >>K2;
    cout << endl;
    return 0;
}
}

double Strangle::Payoff(double z)
{
    if (z>K2) return z-K2;
    else if(z<=K1) return K1-z;
    return 0.0;
}

int Strangle::GetInputData(){
    {
    cout << "Enter Strangle option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K1: "; cin >>K1;
    cout << "Enter strike price K2: "; cin >>K2;
    cout << endl;
    return 0;
}
}

double Butterfly::Payoff(double z)
{
    if (K1<z<=(K2+K1)/2) return z-K1;
    else if((K2+K1)/2<z<=K2) return K2-z;
    return 0.0;
}

int Butterfly::GetInputData(){
    {
    cout << "Enter Butterfly option data: "<<endl;
    int N;
    cout << "Enter steps to expiry N: "; cin >> N;
    SetN(N);
    cout << "Enter strike price K1: "; cin >>K1;
    cout << "Enter strike price K2: "; cin >>K2;
    cout << endl;
    return 0;
}
}