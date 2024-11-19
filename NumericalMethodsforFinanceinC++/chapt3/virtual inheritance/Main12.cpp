#include "BinModel02.h"
#include "Options08.h"
#include <iostream>
#include <cmath>

using namespace std;

int main(){
    BinModel Model;

    if (Model.GetInputData()==1) return 1;

    Call Option1;
    Option1.GetInputData();
    cout << "American call option price = "
    << Option1.PriceBySnell(Model)
    << endl << endl;

    Put Option2;
    Option2.GetInputData();
    cout << "American put option price = "
    << Option2.PriceBySnell(Model)
    << endl << endl;

    char x; cin >> x;
    return 0;
}