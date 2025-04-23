from .translator import SimulationModelGenerator
from ..equation import Equation
import sympy as sp
import re
import os

class CppSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time, name_file, numerical_method="euler"):
        super().__init__(equations, conditionals, initial_state, simulation_time, name_file, numerical_method)
        self.operators = {"sin": "std::sin", "cos": "std::cos", "tan": "std::tan", "exp": "std::exp", "log": "std::log", "sqrt": "std::sqrt"}
        self.pattern_pow = r'([a-zA-Z_][a-zA-Z_0-9]*(?:\[[^\]]+\])?|\(.+?\))\s*\*\*\s*(\d+(?:\.\d+)?)'

    def generate_file(self):
        # Create the C++ simulation file in the folder ./models/
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.cpp", "w")

        self.set_var_identifiers()
        self.set_constants()

        # Write the file
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()

        # Add the integration method
        if self.numerical_method == "euler":
            self.write_euler_method()
        elif self.numerical_method == "runge-kutta-4":
            self.write_runge_kutta_4_method()
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.write_runge_kutta_fehlberg_method()

        self.write_main()

    def prepare_equations(self, equation, subs_dict):
        # Reemplazamos las variables por su cadena inp y el índice correspondiente.
        eq = equation.get_equation().subs(subs_dict)

        # Sustituimos las expresiones x**n a pow(x,n)            
        eq = re.sub(self.pattern_pow, r'pow(\1, \2)', str(eq))

        # Reemplazamos los operadores por los correspondientes en C++.
        for operator, replacement in self.operators.items():
            eq = eq.replace(operator, replacement)

        return eq

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

        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("double tol = 1e-6; // Tolerance for RKF45\n")
            

        # Añadimos las constantes de las ecuaciones y sus valores.
        self.file.write("// Model parameters\n")

        #Lista para comprobar si la constante ya ha sido añadida al archivo.
        list_constants = []      

        #Lista para comprobar si la variable es un resultado de una condición.                   
        eq_conds= self.equations+self.conditionals
        
        for equation in eq_conds:
            constant_values = equation.get_constants_values()  
            
            for constant in equation.get_constants():
                if constant not in list_constants:
                    list_constants.append(constant)
                    value= constant_values.get(constant, 0.0)
                    self.file.write(f"double {constant} = {value};\n")
                            
        self.file.write("\n")

        # Add simulation time parameters
        self.file.write(f"double t0 = {self.simulation_time[0]};\n")
        self.file.write(f"double tf = {self.simulation_time[1]};\n")
        self.file.write(f"double dt = {self.simulation_time[2]};\n")
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("vector<double> t = {t0};\n")
        self.file.write("\n")

        # Add storage for results
        self.file.write("vector<vector<double>> est(n_equations);\n\n")

    def write_conditionals(self):
        # Add the conditions that will be applied to the equations
        self.file.write("\t// Conditions\n")
        
        for i, condition in enumerate(self.conditionals):
            symbols = condition.get_symbols()
            conds = condition.get_conditions()
            results = condition.get_result()

            subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}

            conds = [cond.subs(subs_dict) for cond in conds]
            results = [res.subs(subs_dict) for res in results]
        
            conds = " && ".join([str(cond) for cond in conds])

            self.file.write(f"\tif ({conds})"+"{\n")
            for result in results:
                self.file.write(f"\t\t{result.lhs} = {result.rhs};\n")
            self.file.write("\t}\n")
        
    def write_equations(self):
        # Write the function header
        self.file.write("vector<double> deriv(const vector<double>& inp) {\n")
        self.file.write("    vector<double> out(n_equations);\n")

        self.write_conditionals()

        # Add equations
        for i, equation in enumerate(self.equations):
            
            symbols = equation.get_symbol()
            
            subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}

            eq= self.prepare_equations(equation, subs_dict)
    
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

    def write_runge_kutta_fehlberg_method(self):
        # Write the Runge-Kutta-Fehlberg method (RKF45)
        self.file.write("void rkf45_step(double tt, const vector<double>& inp, double hh, vector<double>& y5, double& error) {\n")
        self.file.write("    const double a[] = {0, 1.0/4, 3.0/8, 12.0/13, 1.0, 1.0/2};\n")
        self.file.write("    const double b[6][5] = {\n")
        self.file.write("        {0, 0, 0, 0, 0},\n")
        self.file.write("        {1.0/4, 0, 0, 0, 0},\n")
        self.file.write("        {3.0/32, 9.0/32, 0, 0, 0},\n")
        self.file.write("        {1932.0/2197, -7200.0/2197, 7296.0/2197, 0, 0},\n")
        self.file.write("        {439.0/216, -8.0, 3680.0/513, -845.0/4104, 0},\n")
        self.file.write("        {-8.0/27, 2.0, -3544.0/2565, 1859.0/4104, -11.0/40}\n")
        self.file.write("    };\n")
        self.file.write("    const double c4[] = {25.0/216, 0, 1408.0/2565, 2197.0/4104, -1.0/5, 0};\n")
        self.file.write("    const double c5[] = {16.0/135, 0, 6656.0/12825, 28561.0/56430, -9.0/50, 2.0/55};\n")
        self.file.write("\n")
        self.file.write("    vector<vector<double>> k(6, vector<double>(n_equations));\n")
        self.file.write("    for (int i = 0; i < 6; ++i) {\n")
        self.file.write("        vector<double> y_temp(n_equations);\n")
        self.file.write("        for (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("            y_temp[j] = inp[j];\n")
        self.file.write("            for (int m = 0; m < i; ++m) {\n")
        self.file.write("                y_temp[j] += hh * b[i][m] * k[m][j];\n")
        self.file.write("            }\n")
        self.file.write("        }\n")
        self.file.write("        k[i] = deriv(y_temp);\n")
        self.file.write("    }\n")
        self.file.write("\n")
        self.file.write("    vector<double> y4(n_equations);\n")
        self.file.write("    y5.resize(n_equations);\n")
        self.file.write("    for (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("        y4[j] = inp[j];\n")
        self.file.write("        y5[j] = inp[j];\n")
        self.file.write("        for (int i = 0; i < 6; ++i) {\n")
        self.file.write("            y4[j] += hh * c4[i] * k[i][j];\n")
        self.file.write("            y5[j] += hh * c5[i] * k[i][j];\n")
        self.file.write("        }\n")
        self.file.write("    }\n")
        self.file.write("\n")
        self.file.write("    error = 0.0;\n")
        self.file.write("    for (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("        error += pow(y5[j] - y4[j], 2);\n")
        self.file.write("    }\n")
        self.file.write("    error = sqrt(error);\n")
        self.file.write("}\n\n")


    def write_main(self):
        # Write the main function
        num_args = 1

        self.file.write("int main(int argc, char* argv[]) {\n")
        self.file.write("    for (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("        est[i].push_back(0.0);\n")  # Initialize with 0.0
        self.file.write("    }\n\n")


        str_symbols = self.get_str_symbols()
        str_time="<t_0> <t_f> <tol>" if self.numerical_method == "runge-kutta-fehlberg" \
                    else "<t_0> <t_f> <d_t>"
        
        #Escribimos la comprobación de los argumentos de la línea de comandos.
        self.file.write(f"\tif (argc < {len(self.constants)+len(self.initial_conditions)+3}) {{ \n")
        self.file.write(f"\t\tcerr << \"Error en el número de parámetros: ./{self.name_file} {str_symbols} \" << \n" \
                        + f"\t\t\" {str_time}   \"<< endl;\n")
        self.file.write("\t\treturn 1;\n \t}\n\n")

        
        for constant in self.constants:
            self.file.write(f"\t{constant}=atof(argv[{num_args}]);\n")
            num_args += 1

        for symbol, value in self.initial_conditions.items():
            self.file.write(f"\test[{self.var_identifiers[symbol]}][0] = atof(argv[{num_args}]);    //{symbol}\n")
            num_args += 1

        self.file.write(f"\tt0 = atof(argv[{num_args}]);\n")
        num_args += 1
        
        self.file.write(f"\ttf = atof(argv[{num_args}]);\n")
        num_args += 1
        
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write(f"\ttol = atof(argv[{num_args}]);\n")
            num_args += 1
        else:
            self.file.write(f"\tdt = atof(argv[{num_args}]);\n")
            num_args += 1

        self.file.write("\n")

        if self.numerical_method == "euler":
            self.file.write("    int steps = static_cast<int>((tf - t0) / dt);\n")
            self.file.write("    for (int i = 1; i <= steps; ++i) {\n")
            self.file.write("        one_step_euler(dt, i);\n")
            self.file.write("    }\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("    int steps = static_cast<int>((tf - t0) / dt);\n")
            self.file.write("    for (int i = 1; i <= steps; ++i) {\n")
            self.file.write("        one_step_runge_kutta_4(dt, i);\n")
            self.file.write("    }\n")
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("    double h = dt;\n")
            self.file.write("    while (t.back() < tf) {\n")
            self.file.write("       vector<double> inp(n_equations);\n")
            self.file.write("       vector<double> y_new;\n")
            self.file.write("       double error;\n\n")
            self.file.write("       for (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("           inp[i] = est[i].back();\n")
            self.file.write("       }\n")
            self.file.write("\n")
           
            self.file.write("       rkf45_step(t.back(), inp, h, y_new, error);\n")
            self.file.write("\n")
            self.file.write("       if (error <= tol) {\n")
            self.file.write("           t.push_back(t.back() + h);\n")
            self.file.write("           for (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("               est[i].push_back(y_new[i]);\n")
            self.file.write("           }\n")
            self.file.write("       }\n")
            self.file.write("\n")
            self.file.write("       // Adjust the step size\n")
            self.file.write("       if (error < 1e-16)\n")
            self.file.write("           error=1e-16;\n\n")
            self.file.write("       h *= min(5.0, max(0.2, 0.84 * pow(tol / error, 0.25)));\n")
            self.file.write("       h = min(h, tf - t.back());\n")
            self.file.write("    }\n")
        

        self.file.write("    // Save the results to a CSV file\n")
        self.file.write(f"    ofstream results(\"{self.name_file}_output_cpp.csv\");\n")
        self.file.write("    results << \"t\";\n")

        # Añadimos los nombres de las variables al archivo CSV.
        for symbol, index in self.var_identifiers.items():
            self.file.write(f"    results << \"\t {symbol}\";\n")
        self.file.write("    results << endl;\n")
       
        #Escribimos los resultados en el archivo CSV en un caso
        # según el método de integración utilizado ya que el método
        # de Runge-Kutta-Fehlberg no tiene un número fijo de pasos.
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("    for (size_t i = 0; i < est[0].size(); ++i) {\n")
            self.file.write("        results << t[i];\n")
        else:
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