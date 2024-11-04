#include <cmath>
#include <iostream>
using namespace std;


double Quad(double x){
    return pow(x,2);
}

class DefInt{
    private:
        double a;
        double b;
        double (*Func) (double x);
    public:
        void SetVals(double a_, double b_, double (*Func_)(double x)){
            a = a_;
            b = b_;
            Func = Func_;
        };
        
        DefInt(){
            SetVals(0.0, 10.0, Quad);
        };

        double ByTrapezoid(int N){
            double h;
            h = (b-a)/N;
            double return_val = 0.0;
            for (int i=0;i<=N;i++){
                if (0<i<N){
                    return_val += 2*Func(a+h*i);
                }
                else{
                    return_val += Func(a+h*i);
                }
            }
            return_val *= h/2;
            return return_val;
        }
};

int main(){
    DefInt MyInt;
    cout << MyInt.ByTrapezoid(1000);
    char x; cin >> x;
    return 0;
}