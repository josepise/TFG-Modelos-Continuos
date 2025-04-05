#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <fstream>
using namespace std;

const int n_equations = 2;

double tol = 1e-6; // Tolerance for RKF45
// Model parameters
const double a = 5;
const double b = 0.05;
const double c = 0.0004;
const double d = 0.2;

const double t0 = 0;
const double tf = 50;
const double dt = 0.1;
vector<double> t = {t0};

vector<vector<double>> est(n_equations);

vector<double> deriv(const vector<double>& inp) {
    vector<double> out(n_equations);
    out[0] = a*inp[0] - b*inp[0]*inp[1];
    out[1] = c*inp[0]*inp[1] - d*inp[1];
    return out;
}

void rkf45_step(double tt, const vector<double>& inp, double hh, vector<double>& y5, double& error) {
    const double a[] = {0, 1.0/4, 3.0/8, 12.0/13, 1.0, 1.0/2};
    const double b[6][5] = {
        {0, 0, 0, 0, 0},
        {1.0/4, 0, 0, 0, 0},
        {3.0/32, 9.0/32, 0, 0, 0},
        {1932.0/2197, -7200.0/2197, 7296.0/2197, 0, 0},
        {439.0/216, -8.0, 3680.0/513, -845.0/4104, 0},
        {-8.0/27, 2.0, -3544.0/2565, 1859.0/4104, -11.0/40}
    };
    const double c4[] = {25.0/216, 0, 1408.0/2565, 2197.0/4104, -1.0/5, 0};
    const double c5[] = {16.0/135, 0, 6656.0/12825, 28561.0/56430, -9.0/50, 2.0/55};

    vector<vector<double>> k(6, vector<double>(n_equations));
    for (int i = 0; i < 6; ++i) {
        vector<double> y_temp(n_equations);
        for (int j = 0; j < n_equations; ++j) {
            y_temp[j] = inp[j];
            for (int m = 0; m < i; ++m) {
                y_temp[j] += hh * b[i][m] * k[m][j];
            }
        }
        k[i] = deriv(y_temp);
    }

    vector<double> y4(n_equations);
    y5.resize(n_equations);
    for (int j = 0; j < n_equations; ++j) {
        y4[j] = inp[j];
        y5[j] = inp[j];
        for (int i = 0; i < 6; ++i) {
            y4[j] += hh * c4[i] * k[i][j];
            y5[j] += hh * c5[i] * k[i][j];
        }
    }

    error = 0.0;
    for (int j = 0; j < n_equations; ++j) {
        error += pow(y5[j] - y4[j], 2);
    }
    error = sqrt(error);
}

int main() {
    for (int i = 0; i < n_equations; ++i) {
        est[i].push_back(0.0);
    }
    est[0][0] = 30;
    est[1][0] = 90;
    double h = dt;
    while (t.back() < tf) {
       vector<double> inp(n_equations);
       for (int i = 0; i < n_equations; ++i) {
           inp[i] = est[i].back();
       }

       if (t.back() + h > tf) {
           h = tf - t.back();
       }
       vector<double> y_new;
       double error;
       rkf45_step(t.back(), inp, h, y_new, error);


       if (error <= tol) {
           t.push_back(t.back() + h);
           for (int i = 0; i < n_equations; ++i) {
               est[i].push_back(y_new[i]);
           }
       }

       h *= min(5.0, max(0.2, 0.84 * pow(tol / error, 0.25)));
       
    cout << scientific << "Tiempo: " << t.back() << " " 
    << "Error: " << error << " Paso: " << h << endl;
    }
    // Save the results to a CSV file
    ofstream results("results.csv");
    results << "Time";
    results << ", x";
    results << ", y";
    results << endl;
    for (size_t i = 0; i < est[0].size(); ++i) {
        results << t[i];
        for (int j = 0; j < n_equations; ++j) {
            results << "	 " << est[j][i];
        }
        results << endl;
    }
    results.close();
    return 0;
}

