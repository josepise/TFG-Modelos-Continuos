from .translator import SimulationModelGenerator
from ..equation import Equation
import sympy as sp
import os

class PythonSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time, path_file ,name_file, output="csv", numerical_method="euler"):
        super().__init__(equations, conditionals,initial_state, simulation_time, path_file, name_file, numerical_method)
        self.operators={"sin":"np.sin", "cos":"np.cos", "tan":"np.tan", "exp":"np.exp", "log":"np.log", "sqrt":"np.sqrt"}
        self.output=output

    def generate_file(self):
        
        #Creamos el archivo de simulación continua en python en la carpeta 
        self.file = open(f"{self.path_file}/{self.name_file}.py", "w")

        #Escribimos el archivo.
        self.set_var_identifiers()
        self.set_constants()
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()
        
        #Añadimos el método de integración.
        if self.numerical_method == "euler":
            self.write_euler_method()
        elif self.numerical_method == "euler-improved":
            self.write_euler_improved_method()
        elif self.numerical_method == "runge-kutta-4":
            self.write_runge_kutta_4_method()
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.write_runge_kutta_fehlberg_method()

        self.write_simulation()
        self.main()
        self.file.close()

    def write_head_file(self):
        #Añadimos los imports necesarios.
        self.file.write("import numpy as np\n")
        self.file.write("import matplotlib.pyplot as plt\n")
        self.file.write("import sys\n")
        self.file.write("\n\n")

    def write_model_parameters(self):
        
        #Añadimos una constante que contenga el número de ecuaciones.
        self.file.write("n_equations = " + str(len(self.equations)) + "\n\n")

        #Añadimos la tolerancia del método de Runge-Kutta-Fehlberg solo
        # en el caso de que .
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("tol = 1e-6\n")

        #Añadimos las constantes de las ecuaciones y sus valores.
        self.file.write("# Parámetros del modelo\n")

        # Añadimos al archivo las constantes .
        for constant in self.constants:
            value = self.constants_values[str(constant)]  
            self.file.write(f"{constant} = {value}\n")
    

        self.file.write("\n\n")

        # Añadimos la variable que cuenta los pasos de tiempo
        self.file.write("iteration = 0\n")

        #Generamos la lista que contendrá los resultados de cada variable en la simulación.
        list_str = f"[{', '.join(['[]' for _ in range(len(self.var_identifiers))])}]"

        self.file.write("est = " + list_str + "\n")
        self.file.write("\n\n")

        #Añadimos las constantes de inicio y fin de la simulación.
        self.file.write(f"t0 = {self.simulation_time[0]}\n")
        self.file.write(f"tf = {self.simulation_time[1]}\n")
        self.file.write(f"dt = {self.simulation_time[2]}\n")
        
        #En caso de que el método de integración sea Runge-Kutta-Fehlberg
        # añadimos la lista que contendrá los pasos de tiempo.
        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("t=[t0]\n")
        else:
            self.file.write("t = np.arange(t0, tf+dt, dt)\n")
        
        self.file.write("\n\n")

    def write_conditionals(self):
        # Añadimos las condiciones que se aplicaran a las ecuaciones.
        self.file.write("\t# Condiciones\n")
        
        # Declaramos los resultados de las condiciones como globales
        list_results=[]
        for condition in self.conditionals:
            for result in condition.get_result():
                if result.lhs not in list_results:
                    list_results.append(result.lhs)
                    self.file.write(f"\tglobal {result.lhs}\n")

        for i, condition in enumerate(self.conditionals):
            symbols = condition.get_symbols()
            conds = condition.get_conditions()
            results = condition.get_result()

            subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}
            
            conds = [cond.subs(subs_dict) for cond in conds]
            results = [res.subs(subs_dict) for res in results]
        
            conds = " and ".join([str(cond) for cond in conds])

            self.file.write(f"\tif {conds}:\n")
            for result in results:
                self.file.write(f"\t\t{result.lhs}={result.rhs}\n")

            self.file.write("\n")
    
            
            

    def write_equations(self):
        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        self.file.write("def deriv(inp):\n")
        
        self.write_conditionals()
    
        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            
            #Sustituimos los simbolos por la cadena inp[i] para poder evaluar la ecuación.
            symbols = equation.get_symbol()
    
            subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}
 
            # Realizamos la sustitución con el diccionario generado
            eq = equation.get_equation().subs(subs_dict)

            # Transformamos la ecuación a una cadena de texto.          
            eq = str(eq)

            # Reemplazamos los operadores por los correspondientes en Python.
            for operator, replacement in self.operators.items():
                eq = eq.replace(operator, replacement)

            #Escribimos la ecuación en el archivo.
            self.file.write(f"\t{equation.get_name()}={eq}\n")
        
        self.file.write("\n")

        # Generamos la cadena que va a ser concatenada a la salida de la función deriv.
        cadena = ""
        

        # Escribmos el nombre de la ecuación como salida en el mismo orden que está en 
        # var_identifiers.
        for var_name in self.var_identifiers.keys():
            for equation in self.equations:
                if var_name == equation.get_name():
                    cadena += f"{equation.get_name()}"
                    if list(self.var_identifiers.keys()).index(var_name) < len(self.var_identifiers) - 1:
                        cadena += ", "
                    break
        #Añadimos la salida de la función deriv.
        self.file.write(f"\treturn [{cadena}]\n")
        self.file.write("\n\n")


    def write_euler_method(self):

        # Añadimos el metodo de Euler para resolver las ecuaciones.
        self.file.write("def one_step_euler(tt, hh, paso):\n")
        self.file.write("    inp = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    out=deriv(inp)\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i].append(inp[i] + (hh * out[i]))\n")
        self.file.write("\n\n")


    def write_euler_improved_method(self):

        #Añadimos el metodo de Euler mejorado para resolver las ecuaciones.
        self.file.write("def one_step_euler_improved(tt, hh, paso):\n")
        self.file.write("    inp = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    out = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    k = [[] for _ in range(n_equations)]\n")
        self.file.write("    for j in range(2):\n")
        self.file.write("       out=deriv(out)\n")
        self.file.write("       for i in range(n_equations):\n")
        self.file.write("           k[i].append(out[i])\n")
        self.file.write("           out[i]=inp[i] + k[i][j] * hh\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i].append(inp[i] + hh*(k[i][0]+k[i][1])/2)\n")
        self.file.write("\n\n")

    def write_runge_kutta_4_method(self):
        # Añadimos el metodo de Runge-Kutta de orden 4 para resolver las ecuaciones.
        self.file.write("def one_step_runge_kutta_4(tt, hh, paso):\n")
        self.file.write("    inp = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    out = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    k = [[] for _ in range(n_equations)]\n")
        self.file.write("    for j in range(4):\n")
        self.file.write("        out=deriv(out)\n")
        self.file.write("        for i in range(n_equations):\n")
        self.file.write("            k[i].append(out[i])\n")
        self.file.write("        if j < 2:\n")
        self.file.write("            incr = hh / 2\n")
        self.file.write("        else:\n")
        self.file.write("            incr = hh\n")
        self.file.write("        for i in range(n_equations):\n")
        self.file.write("            out[i] = inp[i] + k[i][j] * incr\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i].append(inp[i] + hh / 6 * (k[i][0] + 2 * k[i][1] + 2 * k[i][2] + k[i][3]))\n")
        self.file.write("\n\n")
    
    def write_runge_kutta_fehlberg_method(self):

        self.file.write("def rkf45_step(tt, inp, hh):\n")
        self.file.write("    a = [0, 1/4, 3/8, 12/13, 1, 1/2]\n")
        self.file.write("    b = [\n")
        self.file.write("        [0, 0, 0, 0, 0],\n")
        self.file.write("        [1/4, 0, 0, 0, 0],\n")
        self.file.write("        [3/32, 9/32, 0, 0, 0],\n")
        self.file.write("        [1932/2197, -7200/2197, 7296/2197, 0, 0],\n")
        self.file.write("        [439/216, -8, 3680/513, -845/4104, 0],\n")
        self.file.write("        [-8/27, 2, -3544/2565, 1859/4104, -11/40]\n")
        self.file.write("    ]\n")
        self.file.write("    c4 = [25/216, 0, 1408/2565, 2197/4104, -1/5, 0]\n")
        self.file.write("    c5 = [16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55]\n")
        self.file.write("    \n")
        self.file.write("    k = []\n")
        self.file.write("    for i in range(6):\n")
        self.file.write("        y_temp = [inp[j] + hh * sum(b[i][m] * k[m][j] for m in range(i)) if i > 0 else inp[j] for j in range(n_equations)]\n")
        self.file.write("        out=deriv(y_temp)\n")
        self.file.write("        k.append(out)\n")
        self.file.write("    \n")
        self.file.write("    y4 = [inp[j] + hh * sum(c4[i] * k[i][j] for i in range(6)) for j in range(n_equations)]\n")
        self.file.write("    y5 = [inp[j] + hh * sum(c5[i] * k[i][j] for i in range(6)) for j in range(n_equations)]\n")
        self.file.write("    \n")
        self.file.write("    error = np.linalg.norm(np.array(y5) - np.array(y4))\n")
        self.file.write("    return y5, error\n")
        self.file.write("\n\n")

    def write_simulation(self):
        self.file.write("def simulation():\n")
        self.file.write("\tglobal iteration\n")
    
        
        if self.numerical_method == "euler":
            self.file.write("\n\tfor i in range(1, len(t)):\n")
            self.file.write("\t\titeration += 1\n")
            self.file.write("\t\tone_step_euler(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "euler-improved":
            self.file.write("\n\tfor i in range(1, len(t)):\n")
            self.file.write("\t\titeration += 1\n")
            self.file.write("\t\tone_step_euler_improved(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("\n\tfor i in range(1, len(t)):\n")
            self.file.write("\t\titeration += 1\n")
            self.file.write("\t\tone_step_runge_kutta_4(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "runge-kutta-fehlberg":
            self.file.write("\th = dt\n")
            self.file.write("\twhile t[-1] < tf:\n")
            self.file.write("\t\tinp = [est[i][-1] for i in range(n_equations)]\n")
            self.file.write("\t\ty_new, error = rkf45_step(t[-1], inp, h)\n")
            self.file.write("\t\t\n")
            self.file.write("\t\tif error <= tol:\n")
            self.file.write("\t\t\tt.append(t[-1] + h)\n")
            self.file.write("\t\t\tfor i in range(n_equations):\n")
            self.file.write("\t\t\t\test[i].append(y_new[i])\n")
            self.file.write("\t\t\n")
            self.file.write("\t\tif(error > 0):\n")
            self.file.write("\t\t\th *= min(5, max(0.2, 0.84 * (tol / error) ** 0.25))\n")
            self.file.write("\t\telse:\n")
            self.file.write("\t\t\th *= 5\n")
            self.file.write("\t\t\n")
            self.file.write("\t\th=min(h, tf - t[-1])\n")


        self.file.write("\n\n")


    def main(self):
        self.file.write("if __name__ == '__main__':\n")
        
        str_symbols = self.get_str_symbols()
        str_time="<t_0> <t_f> <tol>" if self.numerical_method == "runge-kutta-fehlberg" \
                    else "<t_0> <t_f> <d_t>"

        # Escribimos la comprobación de los argumentos de la línea de comandos.
        self.file.write("\tif len(sys.argv) < " + str(len(self.constants) + len(self.initial_conditions) + 3) + ":\n")
        self.file.write(f"\t\tprint(f\"Error en el número de parámetros: python {{sys.argv[0]}} {str_symbols} {str_time}\")\n")
        self.file.write("\t\tsys.exit(1)\n\n")

        # Añadimos la asignación de los argumentos de la línea de comandos a las variables.
        num_args = 1

        for constant in self.constants:
            self.file.write(f"\t{constant} = float(sys.argv[{num_args}])\n")
            num_args += 1

        for symbol, value in self.initial_conditions.items():
            self.file.write(f"\test[{self.var_identifiers[symbol]}].append(float(sys.argv[{num_args}]))  # {symbol}\n")
            num_args += 1

        self.file.write(f"\tt0 = float(sys.argv[{num_args}])\n")
        num_args += 1

        self.file.write(f"\ttf = float(sys.argv[{num_args}])\n")
        num_args += 1

        if self.numerical_method == "runge-kutta-fehlberg":
            self.file.write(f"\ttol = float(sys.argv[{num_args}])\n")
            num_args += 1
        else:
            self.file.write(f"\tdt = float(sys.argv[{num_args}])\n")
            num_args += 1
        
        self.file.write("\tsimulation()\n")
        self.file.write("\n")

        if self.output == "csv":
            self.write_results()
        elif self.output == "plot":
            self.plot_results()


    def plot_results(self):

        for symbol, index in self.var_identifiers.items():
            self.file.write(f"\tplt.plot(t, est[{index}], label='{symbol}')\n")

        self.file.write("\tplt.show()\n")
        self.file.write("\n\n")
    
    def write_results(self):
        # Añadimos la salida de las variables en el archivo.
        self.file.write("\t# Guardamos los resultados en un archivo de texto\n")
        self.file.write(f"\twith open('{self.name_file}_output_py.csv', 'w') as f:\n")
        self.file.write("\t\t# Escribimos la cabecera del archivo\n")
        self.file.write("\t\tf.write('t\t')\n")
        for symbol in self.var_identifiers.keys():
            self.file.write(f"\t\tf.write('{symbol}\\t')\n")
        self.file.write("\t\tf.write('\\n')\n")
        self.file.write("\t\tfor i in range(len(t)):\n")
        self.file.write("\t\t\tf.write(f'{t[i]} ")
        
        # Creamos una cadena en la que esten separadas est[indice][i] por tabuladores
        # necesaria para el formato csv.
        cadena = "\t"
        for symbol, index in self.var_identifiers.items():
            cadena += "{"+ f"est[{index}]"+"[i]"+"}"    
            cadena += "\t"

        self.file.write(f"{cadena} \\n')\n")

    def compile(self):
        # No se necesita compilación para scripts de Python
        pass

    def run(self):
        # Run the Python script with the required arguments
        os.system(f"python {self.directory}{self.name_file}.py \
                 {' '.join(map(str, self.constants_values.values()))} \
                 {' '.join(map(str, self.initial_conditions.values()))} \
                 {self.simulation_time[0]} {self.simulation_time[1]} {self.simulation_time[2]}")