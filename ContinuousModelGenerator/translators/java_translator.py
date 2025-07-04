from .translator import SimulationModelGenerator
import os
import subprocess
import re
import sympy as sp


class JavaSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time,path_file, name_file, numerical_method="euler"):
        super().__init__(equations, conditionals,initial_state, simulation_time, path_file, name_file, numerical_method)
        self.operators = {"sin": "Math.sin", "cos": "Math.cos", "tan": "Math.tan", "exp": "Math.exp", "log": "Math.log", "sqrt": "Math.sqrt"}
        self.pattern_pow = r'(inp\.get\(\d+\))\s*\*\*\s*(\d+)'

    def generate_file(self):
        if os.name == "nt":
            self.file = open(f"{self.path_file}/{self.name_file}.java", "w")
        else:
            self.file = open(f"{self.path_file}/{self.name_file}", "w")
        # Write the file

        self.set_var_identifiers()
        self.set_constants()
        self.write_head_file()
        self.write_model_parameters()
        self.write_pair_class()
        self.write_equations()

        # Add the integration method
        if self.numerical_method == "euler":
            self.write_euler_method()
        elif self.numerical_method == "euler-improved":
            self.write_euler_improved_method()
        elif self.numerical_method == "runge-kutta-4":
            self.write_runge_kutta_4_method()
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.write_runge_kutta_fehlberg_method()

        self.write_main()
        self.file.close()

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
        if os.name != "nt":
            name_file=self.name_file[:-5]
        else:
            name_file = self.name_file
        self.file.write(f"public class {name_file}" + "{ \n")
        self.file.write(f"\tpublic static final int n_equations = {len(self.equations)};\n\n")

        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\tpublic static double tol = 1e-6; // Tolerance for RKF45\n")

        self.file.write("\t// Model parameters\n")

        for constant in self.constants:
            value = self.constants_values[str(constant)]
            self.file.write(f"\tpublic static double {constant} = {value};\n")
                                    
        self.file.write("\n")

        self.file.write(f"\tpublic static double t0 = {self.simulation_time[0]};\n")
        self.file.write(f"\tpublic static double tf = {self.simulation_time[1]};\n")
        self.file.write(f"\tpublic static double dt = {self.simulation_time[2]};\n")
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

        self.write_conditionals()

        for i, equation in enumerate(self.equations):
            symbols = equation.get_symbol()
            
            subs_dict = {str(sym): sp.Symbol(f"inp.get({self.var_identifiers[str(sym)]})") for sym in symbols}

            eq = self.prepare_equations(equation, subs_dict)
            self.file.write(f"\t\tDouble {equation.get_name()}={eq};\n")

        cadena = self.get_return_values()

        #Añadimos la salida de la función deriv.
        self.file.write(f"\t\treturn Arrays.asList({cadena});\n")
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
        self.file.write("\t\t}\n\n")

        str_symbols = self.get_str_symbols()
        str_time = "<t_0> <t_f> <tol>" if self.numerical_method == "runge-kutta-fehlberg" else "<t_0> <t_f> <d_t>"

        # Calculamos el número de argumentos para cada modo
        min_args_direct = len(self.constants) + len(self.initial_conditions) + 3
        min_args_file = 4  # programa + archivo + t_start + t_end + (tol o dt)

        # Comprobación de argumentos: modo archivo de parámetros
        self.file.write(f"\t\tif (args.length == {min_args_file}) {{\n")
        self.file.write("\t\t\ttry {\n")
        self.file.write("\t\t\t\tList<String> lines = new ArrayList<>();\n")
        self.file.write("\t\t\t\ttry (BufferedReader paramFile = new BufferedReader(new FileReader(args[0]))) {\n")
        self.file.write("\t\t\t\t\tString line;\n")
        self.file.write("\t\t\t\t\twhile ((line = paramFile.readLine()) != null) {\n")
        self.file.write("\t\t\t\t\t\tline = line.trim();\n")
        self.file.write("\t\t\t\t\t\tif (!line.isEmpty()) {\n")
        self.file.write("\t\t\t\t\t\t\tlines.add(line);\n")
        self.file.write("\t\t\t\t\t\t}\n")
        self.file.write("\t\t\t\t\t}\n")
        self.file.write("\t\t\t\t}\n")
        self.file.write(f"\t\t\t\tif (lines.size() < {len(self.constants) + len(self.initial_conditions)}) {{\n")
        self.file.write(f"\t\t\t\t\tSystem.out.println(\"Error: El archivo debe contener {len(self.constants) + len(self.initial_conditions)} valores\");\n")
        self.file.write("\t\t\t\t\tSystem.exit(1);\n")
        self.file.write("\t\t\t\t}\n")
        
        param_index = 0
        for constant in self.constants:
            self.file.write(f"\t\t\t\t{constant} = Double.parseDouble(lines.get({param_index}));\n")
            param_index += 1
        for symbol, value in self.initial_conditions.items():
            self.file.write(f"\t\t\t\test.get({self.var_identifiers[symbol]}).set(0, Double.parseDouble(lines.get({param_index}))); // {symbol}\n")
            param_index += 1
        
        self.file.write("\t\t\t\tt0 = Double.parseDouble(args[1]);\n")
        self.file.write("\t\t\t\ttf = Double.parseDouble(args[2]);\n")
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\t\t\t\ttol = args.length > 3 ? Double.parseDouble(args[3]) : 1e-6;\n")
        else:
            self.file.write("\t\t\t\tdt = args.length > 3 ? Double.parseDouble(args[3]) : 0.01;\n")
        
        self.file.write("\t\t\t} catch (FileNotFoundException e) {\n")
        self.file.write("\t\t\t\tSystem.out.println(\"Error: No se pudo encontrar el archivo \" + args[0]);\n")
        self.file.write("\t\t\t\tSystem.exit(1);\n")
        self.file.write("\t\t\t} catch (NumberFormatException | IndexOutOfBoundsException e) {\n")
        self.file.write("\t\t\t\tSystem.out.println(\"Error: Formato incorrecto en el archivo de parametros\");\n")
        self.file.write("\t\t\t\tSystem.exit(1);\n")
        self.file.write("\t\t\t}\n")

        # Comprobación de argumentos: modo parámetros directos
        self.file.write(f"\t\t}} else if (args.length == {min_args_direct}) {{\n")
        self.file.write("\t\t\tint numArgs = 0;\n\n")

        for constant in self.constants:
            self.file.write(f"\t\t\t{constant} = Double.parseDouble(args[numArgs++]);\n")

        for symbol, value in self.initial_conditions.items():
            self.file.write(f"\t\t\test.get({self.var_identifiers[symbol]}).set(0, Double.parseDouble(args[numArgs++])); // {symbol}\n")

        self.file.write("\t\t\tt0 = Double.parseDouble(args[numArgs++]);\n")
        self.file.write("\t\t\ttf = Double.parseDouble(args[numArgs++]);\n")

        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\t\t\ttol = Double.parseDouble(args[numArgs++]);\n\n")
        else:
            self.file.write("\t\t\tdt = Double.parseDouble(args[numArgs++]);\n\n")
        
        if os.name == "nt":
            name_file=self.name_file
        else:
            name_file=self.name_file[:-5]

        # Mensaje de error para número incorrecto de argumentos
        self.file.write("\t\t} else {\n")
        self.file.write("\t\t\tSystem.out.println(\"Error en el numero de parametros:\");\n")
        self.file.write(f"\t\t\tSystem.out.println(\"Modo 1: java {name_file} {str_symbols} {str_time}\");\n")
        self.file.write(f"\t\t\tSystem.out.println(\"Modo 2: java {name_file} archivo_parametros.txt {str_time}\");\n")
        self.file.write(f"\t\t\tSystem.out.println(\"Modo 2: El orden de los parametros debe ser igual que el de entrada por argumentos y por filas\");\n")
        self.file.write("\t\t\tSystem.exit(1);\n")
        self.file.write("\t\t}\n\n")

        # Resto del código de simulación
        if self.numerical_method == "euler":
            self.file.write("\t\tint steps = (int) ((tf - t0) / dt);\n")
            self.file.write("\t\tfor (int i = 1; i <= steps; ++i) {\n")
            self.file.write("\t\t\toneStepEuler(dt, i);\n")
            self.file.write("\t\t}\n")
        elif self.numerical_method == "euler-improved":
            self.file.write("\t\tint steps = (int) ((tf - t0) / dt);\n")
            self.file.write("\t\tfor (int i = 1; i <= steps; ++i) {\n")
            self.file.write("\t\t\toneStepEulerImproved(dt, i);\n")
            self.file.write("\t\t}\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("\t\tint steps = (int) ((tf - t0) / dt);\n")
            self.file.write("\t\tfor (int i = 1; i <= steps; ++i) {\n")
            self.file.write("\t\t\toneStepRungeKutta4(dt, i);\n")
            self.file.write("\t\t}\n")
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\t\tdouble h = dt;\n")
            self.file.write("\t\twhile (t.get(t.size() - 1) < tf) {\n")
            self.file.write("\t\t\tList<Double> inp = new ArrayList<>(n_equations);\n")
            self.file.write("\t\t\tList<Double> y_new = new ArrayList<>(n_equations);\n")
            self.file.write("\t\t\tdouble error;\n\n")
            self.file.write("\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("\t\t\t\tinp.add(est.get(i).get(est.get(i).size() - 1));\n")
            self.file.write("\t\t\t}\n")
            self.file.write("\n")
            self.file.write("\t\t\tPair<List<Double>, Double> result = rkf45Step(h, inp);\n")
            self.file.write("\t\t\ty_new = result.getKey();\n")
            self.file.write("\t\t\terror = result.getValue();\n")
            self.file.write("\n")
            self.file.write("\t\t\tif (error <= tol) {\n")
            self.file.write("\t\t\t\tt.add(t.get(t.size() - 1) + h);\n")
            self.file.write("\t\t\t\tfor (int i = 0; i < n_equations; ++i) {\n")
            self.file.write("\t\t\t\t\test.get(i).add(y_new.get(i));\n")
            self.file.write("\t\t\t\t}\n")
            self.file.write("\t\t\t}\n")
            self.file.write("\n")
            self.file.write("\t\t\th *= Math.min(5.0, Math.max(0.2, 0.84 * Math.pow(tol / error, 0.25)));\n")
            self.file.write("\t\t\th = Math.min(h, tf - t.get(t.size() - 1));\n")
            self.file.write("\t\t}\n")

        self.file.write("\t\t// Save the results to a CSV file\n")
        self.file.write(f"\t\ttry (BufferedWriter results = new BufferedWriter(new FileWriter(\"{self.name_file}_output_java.csv\"))) {{\n")
        self.file.write("\t\t\tresults.write(\"t\");\n")

        for symbol, index in self.var_identifiers.items():
            self.file.write(f"\t\t\tresults.write(\"\\t {symbol}\");\n")
        self.file.write("\t\t\tresults.newLine();\n")

        self.file.write("\t\t\tfor (int i = 0; i < est.get(0).size(); ++i) {\n")
        
        # En el caso de que el método sea runge-kutta-fehlberg, se guarda el tiempo en la lista t
        # por lo que para mostrarlo en el archivo de salida se utiliza t.get(i).
        # En los demás métodos se utiliza t0 + i * dt ya que el paso de tiempo es constante.
        if self.numerical_method == "runge-kutta-fehlberg":    
            self.file.write("\t\t\t\tresults.write(t.get(i).toString());\n")
        else:
            self.file.write("\t\t\t\tresults.write(String.valueOf(t0 + i * dt));\n")

        self.file.write("\t\t\t\tfor (int j = 0; j < n_equations; ++j) {\n")
        self.file.write("\t\t\t\t\tresults.write(\"\\t\" + est.get(j).get(i));\n")
        self.file.write("\t\t\t\t}\n")
        self.file.write("\t\t\t\tresults.newLine();\n")
        self.file.write("\t\t\t}\n")
        self.file.write("\t\t}\n")

        self.file.write("\t}\n")
        self.file.write("}\n")

    def compile(self):
        flags = 0
        if os.name == "nt":  # "nt" es Windows
            flags = subprocess.CREATE_NO_WINDOW
        else:
            #Quitamos del nombre del archivo la extensión .java si existe
            if self.name_file.endswith('.java'):
                self.name_file = self.name_file[:-5]

        command = [
            "javac",
            f"{self.path_file}/{self.name_file}.java"
        ]
        subprocess.run(command, creationflags=flags)
       

    def run(self,args=None):

        flags = 0
        if os.name == "nt":  # "nt" es Windows
            flags = subprocess.CREATE_NO_WINDOW

        command = [
            "java", "-cp", self.path_file, self.name_file
        ] + args.split()
        
        
        subprocess.run(command, creationflags=flags)
        
