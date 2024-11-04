#include "BinModel01.h"
#include "Options03.h"
#include <iostream>
#include <cmath>
using namespace std;

int main()
{
    double S0, U, D, R;

    if (GetInputData(S0,U,D,R) == 1) return 1;


    double* K[2];
    int N;
    
    cout << "Enter call option data: " << endl;
    GetInputData(N,K);
    cout << "European call option price = "
    << PriceByCRR(S0,U,D,R,N,*K,CallPayoff)
    << endl << endl;

    cout << "Enter put option data: " << endl;
    GetInputData(N,K);
    cout << "European put option price = "
    << PriceByCRR(S0,U,D,R,N,*K,PutPayoff)
    << endl << endl;

    /*Exercise 1.11*/
    cout << "Enter double digital option data: " << endl;
    GetInputData(N,K);
    cout << "European double digital option price = "
    << PriceByCRR(S0,U,D,R,N,*K,PutPayoff)
    << endl << endl;

    /*Exercise 1.9/1.10 digital options*/

    /*
    cout << "Enter digital call option data: " << endl;
    GetInputData(N,K);
    cout << "European digital call option price = "
    << PriceByCRR(S0,U,D,R,N,K,DigCallPayoff)
    << endl << endl;

    cout << "Enter digital put option data: " << endl;
    GetInputData(N,K);
    cout << "European digital put option price = "
    << PriceByCRR(S0,U,D,R,N,K,DigPutPayoff)
    << endl << endl;
    */
    char x; cin >> x;

    return 0;

}