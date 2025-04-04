from .translator import SimulationModelGenerator
from ..equation import Equation
import sympy as sp
import os

class PythonSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, simulation_time, name_file, output, numerical_method="euler"):
        super().__init__(equations, conditionals,initial_state, simulation_time, name_file, numerical_method)
        self.operators={"sin":"np.sin", "cos":"np.cos", "tan":"np.tan", "exp":"np.exp", "log":"np.log", "sqrt":"np.sqrt"}
        self.output=output

    def generate_file(self):
        
        #Creamos el archivo de simulación continua en python en la carpeta 
        # ../models/name_file.py.
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.py", "w")

        #Escribimos el archivo.
        self.set_var_identifiers()
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

        self.write_simulation()
        self.main()

    def write_head_file(self):
        #Añadimos los imports necesarios.
        self.file.write("import numpy as np\n")
        self.file.write("import matplotlib.pyplot as plt\n")
        self.file.write("\n\n")

    def write_model_parameters(self):
        
        #Añadimos una constante que contenga el número de ecuaciones.
        self.file.write("n_equations = " + str(len(self.equations)) + "\n\n")

        #Añadimos las constantes de las ecuaciones y sus valores.
        self.file.write("# Parámetros del modelo\n")

        list_constants = []
        for equation in self.equations:
            constant_values = equation.get_constants_values()

            # Comprobamos si hay mas de una constante y las añadimos al archivo.
            # En caso de que haya una sola constante, la añadimos directamente.
            try:
                for constant in equation.get_constants():
                    if constant not in list_constants:
                        list_constants.append(constant)
                        value = constant_values[str(constant)]  # Convertimos la constante a string si es necesario
                        self.file.write(f"{constant} = {value}\n")
            except:
                
                constant = equation.get_constants()
                if constant not in list_constants:
                    list_constants.append(constant)
                    value = constant_values[str(constant)]
                    self.file.write(f"{equation.get_constants()} = {value}\n")

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
        self.file.write("t = np.arange(t0, tf, dt)\n")
        self.file.write("\n\n")

    def write_initialization_method(self):
        self.file.write("def initialize():\n")
        self.file.write("    iteration = 0\n")

        # Crear una lista basada en el número de ecuaciones
        # Comprobamos que no obtenemos un error con len(self.equations[0].get_simbol))
        try:
            n = len(self.equations[0].get_simbol())
        except:
            n = 1

        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

        self.file.write("est = " + list_str + "\n")
        self.file.write("\n\n")


    def write_equations(self):
        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        self.file.write("def deriv(inp):\n")
        
    
        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            
            #Sustituimos los simbolos por la cadena inp[i] para poder evaluar la ecuación.
            symbols = equation.get_simbol()
    

            try:
                subs_dict = {str(sym): sp.Symbol(f'inp[{self.var_identifiers[str(sym)]}]') for sym in symbols}
            except:
                subs_dict = {str(symbols): sp.Symbol(f'inp[{self.var_identifiers[str(symbols)]}]')}
 
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
        
        #Escribimos la salida de la función deriv en el mismo orden que queda descrita en
        # var_identifiers.
        # for var_name in self.var_identifiers.keys():
        #     cadena += f"{var_name}"
        #     if list(self.var_identifiers.keys()).index(var_name) < len(self.var_identifiers) - 1:
        #         cadena += ", "

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
        self.file.write("    out=deriv(inp)\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i].append(inp[i] + (hh * out[i]))\n")
        self.file.write("    inp = [est[i][paso] for i in range(n_equations)]\n")
        self.file.write("    out=deriv(inp)\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i][paso] = est[i][paso-1] + (hh * out[i])\n")
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
    
    # def write_runge_kutta_fehlberg_method(self):


    def write_simulation(self):
        self.file.write("def simulation():\n")
        self.file.write("\tglobal iteration\n")
        
        #Añadimos las condiciones iniciales.
        for i, symbol in enumerate(self.initial_conditions):
            self.file.write(f"\test[{self.var_identifiers[symbol]}].append({self.initial_conditions[symbol]})\n")
        
        self.file.write("\n\tfor i in range(1, len(t)):\n")
        self.file.write("\t\titeration += 1\n")
        
        if self.numerical_method == "euler":
            self.file.write("\t\tone_step_euler(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "euler-improved":
            self.file.write("\t\tone_step_euler_improved(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("\t\tone_step_runge_kutta_4(t[i-1], dt, iteration)\n")

        self.file.write("\n\n")


    def main(self):
        self.file.write("if __name__ == '__main__':\n")
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
        self.file.write("\twith open('results.csv', 'w') as f:\n")
        self.file.write("\t\tfor i in range(len(t)):\n")
        self.file.write("\t\t\tf.write(f'{t[i]} ")
        
        # Creamos una cadena en la que esten separadas est[indice][i] por tabuladores
        # necesaria para el formato csv.
        cadena = "\t"
        for symbol, index in self.var_identifiers.items():
            cadena += "{"+ f"est[{index}]"+"[i]"+"}"    
            cadena += "\t"

        self.file.write(f"{cadena} \\n')\n")

