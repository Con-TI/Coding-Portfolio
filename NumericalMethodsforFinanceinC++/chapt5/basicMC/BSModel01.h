#ifndef BSModel01_h
#define BSModel01_h

using namespace std;

#include <vector>
#include <ctime>
#include <random>

// Declares a new type, SamplePath, so instead of vector<double> x, we can call SamplePath x.
typedef vector<double> SamplePath;

// r is the risk free rate, sigma is vol, and s0 is initial price
class BSModel{
    public:
    double S0, r, sigma;
    BSModel(double S0_, double r_, double sigma_){
        S0 = S0_; r = r_; sigma = sigma_; srand(time(NULL));
    }
    void GenerateSamplePath(double T, int m, SamplePath& S);
};

#endif