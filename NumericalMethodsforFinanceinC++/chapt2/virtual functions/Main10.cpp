#include "BinModel02.h"
#include "Options06.h"
#include <iostream>
#include <cmath>

using namespace std;

int main(){
    BinModel Model;

    if (Model.GetInputData()==1) return 1;

    Call Option1;
    Option1.GetInputData();
    cout << "European call option price = "
    << Option1.PriceByCRR(Model)
    << endl << endl;

    Put Option2;
    Option2.GetInputData();
    cout << "European put option price = "
    << Option2.PriceByCRR(Model)
    << endl << endl;

    BullSpread Option3;
    Option3.GetInputData();
    cout << "BullSpread option price = "
    << Option3.PriceByCRR(Model)
    << endl << endl;

    BearSpread Option4;
    Option4.GetInputData();
    cout << "BearSpread option price = "
    << Option4.PriceByCRR(Model)
    << endl << endl;

    Strangle Option5;
    Option5.GetInputData();
    cout << "BullSpread option price = "
    << Option5.PriceByCRR(Model)
    << endl << endl;

    Butterfly Option6;
    Option6.GetInputData();
    cout << "BearSpread option price = "
    << Option6.PriceByCRR(Model)
    << endl << endl;

    char x; cin >> x;

    return 0;
}