#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <fstream>
using namespace std;

const int n_equations = 2;

// Model parameters
const double a = 5;
const double b = 0.05;
const double c = 0.0004;
const double d = 0.2;

const double t0 = 0;
const double tf = 50;
const double dt = 0.1;

vector<vector<double>> est(n_equations);

vector<double> deriv(const vector<double>& inp) {
    vector<double> out(n_equations);
    out[0] = a*inp[0] - b*inp[0]*inp[1];
    out[1] = c*inp[0]*inp[1] - d*inp[1];
    return out;
}

void one_step_runge_kutta_4(double hh, int step) {
    vector<double> inp(n_equations);
    for (int i = 0; i < n_equations; ++i) {
        inp[i] = est[i][step - 1];
    }
    vector<vector<double>> k(4, vector<double>(n_equations));
    for (int j = 0; j < 4; ++j) {
        vector<double> out = deriv(inp);
        for (int i = 0; i < n_equations; ++i) {
            k[j][i] = out[i];
        }
        double incr = (j < 2) ? hh / 2 : hh;
        for (int i = 0; i < n_equations; ++i) {
            inp[i] = est[i][step - 1] + k[j][i] * incr;
        }
    }
    for (int i = 0; i < n_equations; ++i) {
        est[i].push_back(est[i][step - 1] + hh / 6 * (k[0][i] + 2 * k[1][i] + 2 * k[2][i] + k[3][i]));
    }
}

int main() {
    for (int i = 0; i < n_equations; ++i) {
        est[i].push_back(0.0);
    }
    est[0][0] = 30;
    est[1][0] = 90;
    int steps = static_cast<int>((tf - t0) / dt);
    for (int i = 1; i <= steps; ++i) {
        one_step_runge_kutta_4(dt, i);
    }
    // Save the results to a CSV file
    ofstream results("results.csv");
    results << "Time";
    results << ", x";
    results << ", y";
    results << endl;
    for (int i = 0; i <= steps; ++i) {
        results << t0 + i * dt;
        for (int j = 0; j < n_equations; ++j) {
            results << "	 " << est[j][i];
        }
        results << endl;
    }
    results.close();
    return 0;
}

