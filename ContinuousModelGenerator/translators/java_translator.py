from .translator import SimulationModelGenerator
import os
import re
import sympy as sp


class JavaSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time, name_file, numerical_method="euler"):
        super().__init__(equations, conditionals, initial_state, simulation_time, name_file, numerical_method)
        self.operators = {"sin": "Math.sin", "cos": "Math.cos", "tan": "Math.tan", "exp": "Math.exp", "log": "Math.log", "sqrt": "Math.sqrt"}
        self.pattern_pow = r'(inp\.get\(\d+\))\s*\*\*\s*(\d+)'

    def generate_file(self):
        # Create the Java simulation file in the folder ./models/
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.java", "w")

        # Write the file
        self.set_var_identifiers()
        self.write_head_file()
        self.write_model_parameters()
        self.write_pair_class()
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
        eq = equation.get_equation().subs(subs_dict)

        eq = re.sub(self.pattern_pow, r'Math.pow(\1, \2)', str(eq))
        
        for operator, replacement in self.operators.items():
            eq = eq.replace(operator, replacement)
        
        return eq

    def write_head_file(self):
        self.file.write("import java.util.*;\n")
        self.file.write("import java.io.*;\n\n")

    def write_pair_class(self):
        self.file.write("\tstatic class Pair<T, U> {\n")
        self.file.write("\t\tprivate T first;\n")
        self.file.write("\t\tprivate U second;\n\n")
        self.file.write("\t\tpublic Pair(T first, U second) {\n")
        self.file.write("\t\t\tthis.first = first;\n")
        self.file.write("\t\t\tthis.second = second;\n")
        self.file.write("\t\t}\n\n")
        self.file.write("\t\tpublic T getKey() {\n")
        self.file.write("\t\t\treturn first;\n")
        self.file.write("\t\t}\n\n")
        self.file.write("\t\tpublic U getValue() {\n")
        self.file.write("\t\t\treturn second;\n")
        self.file.write("\t\t}\n\n")
        self.file.write("\t}\n\n")

    def write_model_parameters(self):
        self.file.write(f"public class {self.name_file}" + "{ \n")
        self.file.write(f"\tpublic static final int n_equations = {len(self.equations)};\n\n")

        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\tpublic static double tol = 1e-6; // Tolerance for RKF45\n")

        self.file.write("\t// Model parameters\n")
        list_constants = []
        list_results_var = [str(var) for condition in self.conditionals for var in condition.get_results_var()]
        eq_conds = self.equations + self.conditionals
        for equation in eq_conds:
            constant_values = equation.get_constants_values()  
           
            for constant in equation.get_constants():
                if constant not in list_constants:
                    list_constants.append(constant)
                    value = constant_values[str(constant)]
                
                    # Comprobamos si alguna de las constantes pueden llegar a cambiar de valor
                    # en el transcurso de la simulación. En caso de ser así, no las declaramos 
                    # como constantes.
                    if constant in list_results_var:
                        self.file.write(f"\tpublic static double {constant} = {value};\n")
                    else:
                        self.file.write(f"\tpublic static final double {constant} = {value};\n")
                    
        self.file.write("\n")

        self.file.write(f"\tpublic static final double t0 = {self.simulation_time[0]};\n")
        self.file.write(f"\tpublic static final double tf = {self.simulation_time[1]};\n")
        self.file.write(f"\tpublic static final double dt = {self.simulation_time[2]};\n")
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\tpublic static List<Double> t = new ArrayList<>(Arrays.asList(t0));\n")
        self.file.write("\n")

        self.file.write("\tpublic static List<List<Double>> est = new ArrayList<>(n_equations);\n\n")

    def write_conditionals(self):
        self.file.write("\t\t// Conditions\n")
        for i, condition in enumerate(self.conditionals):
            symbols = condition.get_symbols()
            conds = condition.get_conditions()
            results = condition.get_result()

            subs_dict = {str(sym): sp.Symbol(f"inp.get({self.var_identifiers[str(sym)]})") for sym in symbols}

            conds = [cond.subs(subs_dict) for cond in conds]
            results = [res.subs(subs_dict) for res in results]

            conds = " && ".join([str(cond) for cond in conds])

            self.file.write(f"\t\tif ({conds}) "+"{\n")
            for result in results:
                self.file.write(f"\t\t\t{result.lhs} = {result.rhs};\n")
            self.file.write("\t\t}\n")

    def write_equations(self):
        self.file.write("\tpublic static List<Double> deriv(List<Double> inp) {\n")
        self.file.write("\t\tList<Double> out = new ArrayList<>(Collections.nCopies(n_equations, 0.0));\n")

        self.write_conditionals()

        for i, equation in enumerate(self.equations):
            symbols = equation.get_symbol()
            
            subs_dict = {str(sym): sp.Symbol(f"inp.get({self.var_identifiers[str(sym)]})") for sym in symbols}

            eq = self.prepare_equations(equation, subs_dict)
            self.file.write(f"\t\tout.set({i}, {eq});\n")

        self.file.write("\t\treturn out;\n")
        self.file.write("\t}\n\n")

    def write_euler_method(self):
        self.file.write("\tpublic static void oneStepEuler(double hh, int step) {\n")
        self.file.write("\t\tList<Double> inp = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\tinp.add(est.get(i).get(step - 1));\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tList<Double> out = deriv(inp);\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\test.get(i).add(inp.get(i) + hh * out.get(i));\n")
        self.file.write("\t\t}\n")
        self.file.write("\t}\n\n")

    def write_euler_improved_method(self):
        self.file.write("\tpublic static void oneStepEulerImproved(double hh, int step) {\n")
        self.file.write("\t\tList<Double> inp = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tList<Double> out = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tList<List<Double>> k = new ArrayList<>();\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\tinp.add(est.get(i).get(step - 1));\n")
        self.file.write("\t\t\tout.add(est.get(i).get(step - 1));\n")
        self.file.write("\t\t\tk.add(new ArrayList<>());\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tfor (int j = 0; j < 2; ++j) {\n")
        self.file.write("\t\t\tout = deriv(out);\n")
        self.file.write("\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\t\tk.get(i).add(out.get(i));\n")
        self.file.write("\t\t\t\tout.set(i, inp.get(i) + k.get(i).get(j) * hh);\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\test.get(i).add(inp.get(i) + hh * (k.get(i).get(0) + k.get(i).get(1)) / 2);\n")
        self.file.write("\t\t}\n")
        self.file.write("\t}\n\n")

    def write_runge_kutta_4_method(self):
        self.file.write("\tpublic static void oneStepRungeKutta4(double hh, int step) {\n")
        self.file.write("\t\tList<Double> inp = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tList<Double> out = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tList<List<Double>> k = new ArrayList<>();\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\tinp.add(est.get(i).get(step - 1));\n")
        self.file.write("\t\t\tout.add(est.get(i).get(step - 1));\n")
        self.file.write("\t\t\tk.add(new ArrayList<>());\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tfor (int j = 0; j < 4; ++j) {\n")
        self.file.write("\t\t\tout = deriv(out);\n")
        self.file.write("\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\t\tk.get(i).add(out.get(i));\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t\tdouble incr = (j < 2) ? hh / 2 : hh;\n")
        self.file.write("\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\t\tout.set(i, inp.get(i) + k.get(i).get(j) * incr);\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\test.get(i).add(inp.get(i) + hh / 6 * (k.get(i).get(0) + 2 * k.get(i).get(1) + 2 * k.get(i).get(2) + k.get(i).get(3)));\n")
        self.file.write("\t\t}\n")
        self.file.write("\t}\n\n")

    def write_runge_kutta_fehlberg_method(self):
        self.file.write("\tpublic static Pair<List<Double>, Double> rkf45Step(double hh, List<Double> inp) {\n")
        self.file.write("\t\tdouble[] a = {0, 1.0 / 4, 3.0 / 8, 12.0 / 13, 1.0, 1.0 / 2};\n")
        self.file.write("\t\tdouble[][] b = {\n")
        self.file.write("\t\t\t{0, 0, 0, 0, 0},\n")
        self.file.write("\t\t\t{1.0 / 4, 0, 0, 0, 0},\n")
        self.file.write("\t\t\t{3.0 / 32, 9.0 / 32, 0, 0, 0},\n")
        self.file.write("\t\t\t{1932.0 / 2197, -7200.0 / 2197, 7296.0 / 2197, 0, 0},\n")
        self.file.write("\t\t\t{439.0 / 216, -8, 3680.0 / 513, -845.0 / 4104, 0},\n")
        self.file.write("\t\t\t{-8.0 / 27, 2, -3544.0 / 2565, 1859.0 / 4104, -11.0 / 40}\n")
        self.file.write("\t\t};\n")
        self.file.write("\t\tdouble[] c4 = {25.0 / 216, 0, 1408.0 / 2565, 2197.0 / 4104, -1.0 / 5, 0};\n")
        self.file.write("\t\tdouble[] c5 = {16.0 / 135, 0, 6656.0 / 12825, 28561.0 / 56430, -9.0 / 50, 2.0 / 55};\n")
        self.file.write("\t\tList<List<Double>> k = new ArrayList<>();\n")
        self.file.write("\t\tfor (int i = 0; i < 6; ++i) {\n")
        self.file.write("\t\t\tList<Double> yTemp = new ArrayList<>(n_equations);\n")
        self.file.write("\t\t\tfor (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("\t\t\t\tdouble sum = 0;\n")
        self.file.write("\t\t\t\tfor (int m = 0; m < i; ++m) {\n")
        self.file.write("\t\t\t\t\tsum += b[i][m] * k.get(m).get(j);\n")
        self.file.write("\t\t\t\t}\n")
        self.file.write("\t\t\t\tyTemp.add(i > 0 ? inp.get(j) + hh * sum : inp.get(j));\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t\tk.add(deriv(yTemp));\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tList<Double> y4 = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tList<Double> y5 = new ArrayList<>(n_equations);\n")
        self.file.write("\t\tfor (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("\t\t\tdouble sum4 = 0, sum5 = 0;\n")
        self.file.write("\t\t\tfor (int i = 0; i < 6; ++i) {\n")
        self.file.write("\t\t\t\tsum4 += c4[i] * k.get(i).get(j);\n")
        self.file.write("\t\t\t\tsum5 += c5[i] * k.get(i).get(j);\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t\ty4.add(inp.get(j) + hh * sum4);\n")
        self.file.write("\t\t\ty5.add(inp.get(j) + hh * sum5);\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\tdouble error = 0;\n")
        self.file.write("\t\tfor (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("\t\t\terror += Math.pow(y5.get(j) - y4.get(j), 2);\n")
        self.file.write("\t\t}\n")
        self.file.write("\t\terror = Math.sqrt(error);\n")
        self.file.write("\t\treturn new Pair<>(y5, error);\n")
        self.file.write("\t}\n\n")

    def write_main(self):
        self.file.write("\tpublic static void main(String[] args) throws IOException {\n")
        self.file.write("\t\tfor (int i = 0; i < n_equations; ++i) {\n")
        self.file.write("\t\t\test.add(new ArrayList<>(Collections.singletonList(0.0)));\n")
        self.file.write("\t\t}\n")

        for symbol, value in self.initial_conditions.items():
            self.file.write(f"\t\t\test.get({self.var_identifiers[symbol]}).set(0, {value:.1f});\n")

        if self.numerical_method == "euler":
            self.file.write("\t\t\tint steps = (int) ((tf - t0) / dt);\n")
            self.file.write("\t\t\tfor (int i = 1; i <= steps; ++i) {\n")
            self.file.write("\t\t\t\toneStepEuler(dt, i);\n")
            self.file.write("\t\t\t}\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("\t\t\tint steps = (int) ((tf - t0) / dt);\n")
            self.file.write("\t\t\tfor (int i = 1; i <= steps; ++i) {\n")
            self.file.write("\t\t\t\toneStepRungeKutta4(dt, i);\n")
            self.file.write("\t\t\t}\n")
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\t\t\tdouble h = dt;\n")
            self.file.write("\t\t\twhile (t.get(t.size() - 1) < tf) {\n")
            self.file.write("\t\t\t\tList<Double> inp = new ArrayList<>(n_equations);\n")
            self.file.write("\t\t\t\tList<Double> y_new = new ArrayList<>(n_equations);\n")
            self.file.write("\t\t\t\tdouble error;\n\n")
            self.file.write("\t\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("\t\t\t\t\tinp.add(est.get(i).get(est.get(i).size() - 1));\n")
            self.file.write("\t\t\t\t}\n")
            self.file.write("\n")
            self.file.write("\t\t\t\tPair<List<Double>, Double> result = rkf45Step(h, inp);\n")
            self.file.write("\t\t\t\ty_new = result.getKey();\n")
            self.file.write("\t\t\t\terror = result.getValue();\n")
            self.file.write("\n")
            self.file.write("\t\t\t\tif (error <= tol) {\n")
            self.file.write("\t\t\t\t\tt.add(t.get(t.size() - 1) + h);\n")
            self.file.write("\t\t\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("\t\t\t\t\t\test.get(i).add(y_new.get(i));\n")
            self.file.write("\t\t\t\t\t}\n")
            self.file.write("\t\t\t\t}\n")
            self.file.write("\n")
            self.file.write("\t\t\t\th *= Math.min(5.0, Math.max(0.2, 0.84 * Math.pow(tol / error, 0.25)));\n")
            self.file.write("\t\t\t\th = Math.min(h, tf - t.get(t.size() - 1));\n")
            self.file.write("\t\t\t}\n")

        self.file.write("\t\t// Save the results to a CSV file\n")
        self.file.write(f"\t\ttry (BufferedWriter results = new BufferedWriter(new FileWriter(\"{self.name_file}_output_java.csv\"))) {{\n")
        self.file.write("\t\t\tresults.write(\"t\");\n")

        for symbol, index in self.var_identifiers.items():
            self.file.write(f"\t\t\tresults.write(\"\t {symbol}\");\n")
        self.file.write("\t\t\tresults.newLine();\n")

        self.file.write("\t\t\tfor (int i = 0; i < est.get(0).size(); ++i) {\n")
        
        #En el caso de que el metodo sea runge-kutta-fehlberg, se guarda el tiempo en la lista t
        #por lo que para mostrarlo en el archivo de salida se utiliza t.get(i).
        #En los demás métodos se utiliza t0 + i * dt ya que el paso de tiempo es constante.
        if self.numerical_method == "runge-kutta-fehlberg":    
            self.file.write("\t\t\t\tresults.write(t.get(i).toString());\n")
        else:
            self.file.write("\t\t\t\tresults.write(String.valueOf(t0+i * dt));\n")

        self.file.write("\t\t\t\tfor (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("\t\t\t\t\tresults.write(\"\\t\" + est.get(j).get(i));\n")
        self.file.write("\t\t\t\t}\n")
        self.file.write("\t\t\t\tresults.newLine();\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t}\n")

        self.file.write("\t}\n")
        self.file.write("}\n")
