#include "BinLattice02.h"
#include "BinModel02.h"
#include "Options09.h"
#include <iostream>
using namespace std;

int main(){
    BinModel Model;

    if (Model.GetInputData() == 1) return 1;

    Put Option1;
    Option1.GetInputData();
    BinLattice<double> PriceTree;
    BinLattice<bool> StoppingTree;

    Option1.PriceBySnell(Model, PriceTree, StoppingTree);
    
    cout << "American put prices: " << endl << endl;
    PriceTree.Display();
    cout << "American put exercise policy" << endl << endl;
    StoppingTree.Display();

    Call Option2;
    Option2.GetInputData();
    BinLattice<double> PortfolioTree; 
    BinLattice<double> MoneyMarketTree;

    Option2.PriceByCRR(Model, PortfolioTree, MoneyMarketTree);

    cout << "European replicating stock portfolio" << endl << endl;
    PortfolioTree.Display();
    cout << "Money Market account" << endl << endl;
    MoneyMarketTree.Display();

    char x; cin >> x;

    return 0;
}