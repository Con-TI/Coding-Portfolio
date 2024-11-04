#include "Solver02.h"
#include <iostream>
using namespace std;

class F1: public Function{
    public:
        double Value(double x) {return x*x - 2;}
        double Deriv(double x) {return 2*x;}
} MyF1;

class F2: public Function{
    private:
        double a;
    public:
        F2(double a_) {a=a_;}
        double Value(double x) {return x*x - a;}
        double Deriv(double x) {return 2*x;}
} MyF2(3.0);
// SOmething wrong with bisect
int main(){
    double Acc = 0.00001;
    double LEnd = 0.0, REnd = 2.0;
    double Tgt = 0.0;
    cout << "Root of F1 by bisect: "
    << SolverByBisect(&MyF1,Tgt,LEnd,REnd,Acc)
    <<endl;
    cout << "Root of F2 by bisect: "
    << SolverByBisect(&MyF2,Tgt,LEnd,REnd,Acc)
    <<endl;
    double Guess = 1.0;
    cout << "Root of F1 by Newton-Raphson: "
    << SolverByNR(&MyF1,Tgt,Guess,Acc)
    <<endl;
    cout << "Root of F2 by Newton-Raphson: "
    << SolverByNR(&MyF2,Tgt,Guess,Acc)
    <<endl;

    char x; cin >> x;

    return 0;
}
