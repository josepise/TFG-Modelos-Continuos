from .translator import SimulationModelGenerator
from ..equation import Equation
import sympy as sp
import os

class CppSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time, name_file, numerical_method="euler"):
        super().__init__(equations, conditionals, initial_state, simulation_time, name_file, numerical_method)
        self.operators = {"sin": "std::sin", "cos": "std::cos", "tan": "std::tan", "exp": "std::exp", "log": "std::log", "sqrt": "std::sqrt"}

    def generate_file(self):
        # Create the C++ simulation file in the folder ./models/
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.cpp", "w")

        # Write the file
        self.set_var_identifiers()
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()

        # Add the integration method
        if self.numerical_method == "euler":
            self.write_euler_method()
        elif self.numerical_method == "runge-kutta-4":
            self.write_runge_kutta_4_method()

        self.write_main()

    def write_head_file(self):
        # Add necessary includes
        self.file.write("#include <iostream>\n")
        self.file.write("#include <vector>\n")
        self.file.write("#include <cmath>\n")
        self.file.write("#include <iomanip>\n")
        self.file.write("#include <fstream>\n")
        self.file.write("using namespace std;\n\n")

    def write_model_parameters(self):
        # Add the number of equations
        self.file.write(f"const int n_equations = {len(self.equations)};\n\n")

        # Add constants for the equations
        self.file.write("// Model parameters\n")
        for equation in self.equations:
            constant_values = equation.get_constants_values()
            try:
                for constant in equation.get_constants():
                    value = constant_values[str(constant)]
                    self.file.write(f"const double {constant} = {value};\n")
            except:
                constant = equation.get_constants()
                value = constant_values[str(constant)]
                self.file.write(f"const double {constant} = {value};\n")
        self.file.write("\n")

        # Add simulation time parameters
        self.file.write(f"const double t0 = {self.simulation_time[0]};\n")
        self.file.write(f"const double tf = {self.simulation_time[1]};\n")
        self.file.write(f"const double dt = {self.simulation_time[2]};\n")
        self.file.write("\n")

        # Add storage for results
        self.file.write("vector<vector<double>> est(n_equations);\n\n")

    def write_equations(self):
        # Write the function header
        self.file.write("vector<double> deriv(const vector<double>& inp) {\n")
        self.file.write("    vector<double> out(n_equations);\n")

        # Add equations
        for i, equation in enumerate(self.equations):
            
            symbols = equation.get_simbol()
            
            try:
                subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}
            except:
                subs_dict = {str(symbols): sp.Symbol(f'inp[{self.var_identifiers[str(symbols)]}]')}

            
            print(f"subs_dict: {subs_dict}")
            eq = equation.get_equation().subs(subs_dict)
            
            eq = str(eq)

            for operator, replacement in self.operators.items():
                eq = eq.replace(operator, replacement)

            self.file.write(f"    out[{i}] = {eq};\n")
           

        self.file.write("    return out;\n")
        self.file.write("}\n\n")

    def write_euler_method(self):
        # Write the Euler method
        self.file.write("void one_step_euler(double hh, int step) {\n")
        self.file.write("    vector<double> inp(n_equations);\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        inp[i] = est[i][step - 1];\n")
        self.file.write("    }\n")
        self.file.write("    vector<double> out = deriv(inp);\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        est[i].push_back(inp[i] + hh * out[i]);\n")
        self.file.write("    }\n")
        self.file.write("}\n\n")

    def write_runge_kutta_4_method(self):
        # Write the Runge-Kutta 4 method
        self.file.write("void one_step_runge_kutta_4(double hh, int step) {\n")
        self.file.write("    vector<double> inp(n_equations);\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        inp[i] = est[i][step - 1];\n")
        self.file.write("    }\n")
        self.file.write("    vector<vector<double>> k(4, vector<double>(n_equations));\n")
        self.file.write("    for (int j = 0; j < 4; ++j) {\n")
        self.file.write("        vector<double> out = deriv(inp);\n")
        self.file.write("        for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("            k[j][i] = out[i];\n")
        self.file.write("        }\n")
        self.file.write("        double incr = (j < 2) ? hh / 2 : hh;\n")
        self.file.write("        for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("            inp[i] = est[i][step - 1] + k[j][i] * incr;\n")
        self.file.write("        }\n")
        self.file.write("    }\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        est[i].push_back(est[i][step - 1] + hh / 6 * (k[0][i] + 2 * k[1][i] + 2 * k[2][i] + k[3][i]));\n")
        self.file.write("    }\n")
        self.file.write("}\n\n")

    def write_main(self):
        # Write the main function
        self.file.write("int main() {\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        est[i].push_back(0.0);\n")  # Initialize with 0.0
        self.file.write("    }\n")

        for symbol, value in self.initial_state.items():
            self.file.write(f"    est[{self.var_identifiers[symbol]}][0] = {value};\n")

        self.file.write("    int steps = static_cast<int>((tf - t0) / dt);\n")
        self.file.write("    for (int i = 1; i <= steps; ++i) {\n")
        if self.numerical_method == "euler":
            self.file.write("        one_step_euler(dt, i);\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("        one_step_runge_kutta_4(dt, i);\n")
        self.file.write("    }\n")

        self.file.write("    // Save the results to a CSV file\n")
        self.file.write("    ofstream results(\"results.csv\");\n")
        self.file.write("    results << \"Time\";\n")
        for symbol, index in self.var_identifiers.items():
            self.file.write(f"    results << \", {symbol}\";\n")
        self.file.write("    results << endl;\n")
        self.file.write("    for (int i = 0; i <= steps; ++i) {\n")
        self.file.write("        results << t0 + i * dt;\n")
        self.file.write("        for (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("            results << \"\t \" << est[j][i];\n")
        self.file.write("        }\n")
        self.file.write("        results << endl;\n")
        self.file.write("    }\n")
        self.file.write("    results.close();\n")

        self.file.write("    return 0;\n")
        self.file.write("}\n\n")