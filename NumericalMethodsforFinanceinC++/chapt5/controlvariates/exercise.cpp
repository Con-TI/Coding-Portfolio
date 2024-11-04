#include <random>
#include <ctime>
#include <cmath>
#include <iostream>

using namespace std;

const double pi = 4.0*atan(1.0);

double Gauss(){
    double U1 = (rand()+1.0)/(RAND_MAX+1.0);
    double U2 = (rand()+1.0)/(RAND_MAX+1.0);
    return sqrt(-2.0*log(U1)) * cos(2.0*pi*U2)/2;
}

// Y is the control variate to X
// This method reduces variance of estimate
int main(){
    srand(time(NULL));
    double E_Y = 7/8;
    double E_X_Y = 0.0;
    for (int i=0; i<10000; i++){
        double z = Gauss();
        E_X_Y = (E_X_Y*i + (cos(z)-1+0.5*pow(z,2)))/(i+1);
    }
    double E_X = E_X_Y + E_Y;
    cout << E_X;
    char x; cin >> x;
    return 0;
}



