#include <iostream>
using namespace std;

template <typename Function> double SolveByTrap(Function Fct, double a, double b, int N){
    double h = (b-a)/N;
    double integral = 0;
    for (int i=0;i<=N;i++){
        if (0<i<N){
            integral += 2*Fct.Value(a+i*h);
        }
        else{
            integral += Fct.Value(a+i*h);
        }
    }
    integral *= h/2;
    return integral;
};

class F{
    public:
        double Value(double x) {return x*x;}
} MyFunc;

int main(){
    cout << "Integral of x^2 between -10 and 10: ";
    cout << SolveByTrap(MyFunc,-2,2,1000);
    char x; cin>>x;
    return 0;
}
