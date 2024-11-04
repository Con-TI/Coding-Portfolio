#include "Options01.h"
#include "BinModel01.h"
#include <iostream>
#include <cmath>
using namespace std;

int GetInputData(int& N, double&K){
    cout<< "Enter Steps to Expiry N: "; cin >> N;
    cout<< "Enter Strike Price K: "; cin >> K;
    cout<<endl;
    /* Exercise 1.4 */
    if ((K<=0) | (N<=0)){
        cout<< "Illegal Data Ranges" <<endl;
        cout<< "Terminating program" <<endl;
        return 1;
    }
    return 0;
}

double PriceByCRR(double S0, double U, double D, double R, int N, double K){
    double q = RiskNeutralProb(U, D, R);
    int fact_N = 1;
    for (int n=1; n<=N; n++){
        fact_N *= n;
    }

    /* Exercise 1.5 CRR direct formula*/
    double Price = 0;
    for (int i=0; i<=N; i++){
        int fact_i = 1;
        for (int n=1; n<=i; n++){
            fact_i *= n;
        }
        int fact_N_i = 1;
        for (int n=1;n<=N-i;n++){
            fact_N_i *= n;
        }
        Price += fact_N/(fact_i*fact_N_i)*pow(q,i)*pow(1-q,N-i)*CallPayoff(S(S0,U,D,N,i), K)/pow(1+R,N);
    }
    return Price;
    
    /*double Price[N+1];
    for (int i=0; i<=N; i++){
        Price[i] = CallPayoff(S(S0,U,D,N,i), K);
    }
    */
   
    /* Exercise 1.3 while loop
    int n = N-1;
    while (n>=0){
        for (int i=0; i<=n; i++){
            Price[i] = (q*Price[i+1]+(1-q)*Price[i])/(1+R);
        }
        n--;
    }
    */

    /* Initial Iterative
    for (int n=N-1; n>=0; n--){
        for (int i=0; i<=n; i++){
            Price[i] = (q*Price[i+1]+(1-q)*Price[i])/(1+R);
        }
    }
    */
    // return Price[0];
}

double CallPayoff(double z, double K){
    if (z>K) return z-K;
    return 0;

}