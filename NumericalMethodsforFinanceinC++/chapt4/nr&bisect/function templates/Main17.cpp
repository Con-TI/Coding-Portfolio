#include "Solver03.h"
#include <iostream>
#include <vector>
using namespace std;


class F1{
    public:
        double Value(double x) {return x*x-2;}
        double Deriv (double x) {return 2*x;}
} MyF1;

class F2{
    private:
        double a;
    public:
        F2(double a_) {a=a_;}
        double Value(double x) {return x*x-a;}
        double Deriv(double x) {return 2*x;}
} MyF2(3.0);

class Coupon{
    private:
        double F;
        double T;
        vector<double> C;
    public:
        Coupon(vector<double> C_, double T_, double F_) {C=C_; T=T_; F=F_;}
        double Value(double y){
            double sum = 0;
            double t = T/C.size();
            for (int i=0; i<C.size();i++){
                sum += C[i]*exp(-y*t*(i+1));
            }
            sum += F*exp(-y*T);
            return sum;
        }
        double Deriv(double y){
            return -1*Value(y);
        }
} MyCoupon({10,14,15,12,13},10,100);

int main(){
    double Acc = 0.001;
    double LEnd = 0.0, REnd = 2.0;
    double Tgt = 0.0;
    cout << "Root of F1 by bisect: "
    << SolveByBisect(MyF1, Tgt, LEnd, REnd, Acc)
    << endl;
    cout << "Root of F2 by bisect: "
    << SolveByBisect(MyF2, Tgt, LEnd, REnd, Acc)
    << endl;
    double Guess=1.0;
    cout << "Root of F1 by Newton-Raphson: "
    << SolveByNR(MyF1, Tgt, Guess, Acc)
    << endl;
    cout << "Root of F2 by Newton-Raphson: "
    << SolveByNR(MyF2, Tgt, Guess, Acc)
    << endl;
    
    Tgt = 100.0;
    LEnd = -100;
    REnd = 100;
    Guess = 0.0;

    cout << "y of Coupon by bisect: "
    << SolveByBisect(MyCoupon, Tgt, LEnd, REnd, Acc)
    << endl;
    cout << "y of Coupon by Newton-Raphson: "
    << SolveByNR(MyCoupon, Tgt, Guess, Acc)
    << endl;
    

    char x; cin >> x;

    return 0;
}