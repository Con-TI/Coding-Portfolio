#include "Matrix.h"
#include <cmath>

// Square matrix C and vector V of dims dxd and d
Vector operator* (const Matrix& C, const Vector& V){
    int d = C.size();
    Vector W(d);
    for (int j=0; j<d; j++){
        W[j] = 0.0;
        for (int l=0; l<d; l++) W[j] = W[j] + C[j][l]*V[l];
    }
    return W;
}

// element wise multiplication
Vector operator* (const double& a, const Vector& V){
    int d = V.size();
    Vector W(d);
    for (int j = 0; j<d; j++){
        W[j] = a*V[j];
    }
    return W;
}

//element wise addition
Vector operator+ (const double& a, const Vector& V){
    int d = V.size();
    Vector W(d);
    for (int j = 0; j<d; j++){
        W[j] = a+V[j];
    }
    return W;
}

//element wise addition
Vector operator+ (const Vector& V, const Vector& W){
    int d = V.size();
    Vector U(d);
    for (int j = 0; j<d; j++){
        U[j] = V[j]+W[j];
    }
    return U;
}

// element wise multiplication
Vector operator* (const Vector & V, const Vector & W){
    int d = V.size();
    Vector U(d);
    for (int j=0; j<d; j++){
        U[j] = V[j]*W[j];
    }
    return U;
}

// element wise natural exp
Vector exp (const Vector& V){
    int d = V.size();
    Vector W(d);
    for (int j=0; j<d; j++){
        W[j] = exp(V[j]);
    }
    return W;
}

Vector operator/ (const Vector& V, const double& a){
    int d = V.size();
    Vector W(d);
    for (int j=0; j<d; j++){
        W[j] = V[j]/a;
    }
    return W;
}

Vector operator/ (const Vector& V, const Vector& W){
    int d = V.size();
    Vector U(d);
    for (int j=0; j<d; j++){
        U[j] = V[j]/W[j];
    }
    return U;
}

// acts as dot product
double operator^ (const Vector& V, const Vector& W){
    double sum =0.0;
    int d = V.size();
    for (int j=0; j<d; j++) sum = sum + V[j]*W[j];
    return sum;
}