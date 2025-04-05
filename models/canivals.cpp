#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <fstream>
using namespace std;

const int n_equations = 4;

long double tol = 1e-6; // Tolerance for RKF45
// Model parameters
const long double a = 2;

const long double t0 = 0;
const long double tf = 10;
const long double dt = 0.1;
vector<long double> t = {t0};

vector<vector<long double>> est(n_equations);

vector<long double> deriv(const vector<long double>& inp) {
    vector<long double> out(n_equations);
    out[0] = a*inp[2] - inp[0]*inp[1] - inp[0];
    out[1] = inp[0] - inp[1]*inp[3] - inp[1];
    out[2] = inp[1] - inp[2]*inp[3] - inp[3];
    out[3] = -inp[2] + inp[3];
    return out;
}

void rkf45_step(long double tt, const vector<long double>& inp, long double hh, vector<long double>& y5, long double& error) {
    const long double a[] = {0, 1.0/4, 3.0/8, 12.0/13, 1.0, 1.0/2};
    const long double b[6][5] = {
        {0, 0, 0, 0, 0},
        {1.0/4, 0, 0, 0, 0},
        {3.0/32, 9.0/32, 0, 0, 0},
        {1932.0/2197, -7200.0/2197, 7296.0/2197, 0, 0},
        {439.0/216, -8.0, 3680.0/513, -845.0/4104, 0},
        {-8.0/27, 2.0, -3544.0/2565, 1859.0/4104, -11.0/40}
    };
    const long double c4[] = {25.0/216, 0, 1408.0/2565, 2197.0/4104, -1.0/5, 0};
    const long double c5[] = {16.0/135, 0, 6656.0/12825, 28561.0/56430, -9.0/50, 2.0/55};

    vector<vector<long double>> k(6, vector<long double>(n_equations));
    for (int i = 0; i < 6; ++i) {
        vector<long double> y_temp(n_equations);
        for (int j = 0; j < n_equations; ++j) {
            y_temp[j] = inp[j];
            for (int m = 0; m < i; ++m) {
                y_temp[j] += hh * b[i][m] * k[m][j];
            }
        }
        k[i] = deriv(y_temp);
    }

    vector<long double> y4(n_equations);
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
    est[0][0] = 1;
    est[1][0] = 0;
    est[3][0] = 0;
    est[2][0] = 0;
    long double h = dt;
    while (t.back() < tf) {
       vector<long double> inp(n_equations);
       vector<long double> y_new;
       long double error;

       for (int i = 0; i < n_equations; ++i) {
           inp[i] = est[i].back();
       }

       rkf45_step(t.back(), inp, h, y_new, error);

       if (error <= tol) {
           t.push_back(t.back() + h);
           for (int i = 0; i < n_equations; ++i) {
               est[i].push_back(y_new[i]);
           }
       }

       // Adjust the step size
       if (error < 1e-16)
           error=1e-16;

       h *= min(5.0, max(0.2, 0.84 * pow(tol / error, 0.25)));
       h = min(h, tf - t.back());
    }
    // Save the results to a CSV file
    ofstream results("canivals_output_cpp.csv");
    results << "Time";
    results << ", p_1";
    results << ", p_2";
    results << ", p_4";
    results << ", p_3";
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

