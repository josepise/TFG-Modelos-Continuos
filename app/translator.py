from abc import ABC, abstractmethod
from equation import Equation
import sympy as sp
import os

class SimulationModelGenerator(ABC):
    

    def __init__(self, equations, conditionals, initial_state, name_file, numerical_method="euler"):
        self.equations = equations
        self.conditionals = conditionals
        self.name_file = name_file
        self.numerical_method = numerical_method
        self.initial_state=initial_state
    
    @abstractmethod
    def generate_file(self):
        pass


    def check_initial_state(self):
        
        #Comprobamos que cada variable de las ecuaciones tenga un valor inicial.
        for equation in self.equations:
            for symbol in equation.get_simbol():
                if symbol not in self.initial_state:
                    raise ValueError(f"La variable {symbol} no tiene un valor inicial asignado.")


        

# Hacemos una clase que genere el archivo de simulación continua en python.

class PythonSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, initial_state, name_file, numerical_method="euler"):
        super().__init__(equations, conditionals,initial_state, name_file, numerical_method)
    

    def generate_file(self):
        
        #Creamos el archivo de simulación continua en python en la carpeta 
        # ../models/name_file.py.
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.py", "w")

        #Escribimos el archivo.
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()
        
        #Añadimos el método de integración.
        if self.numerical_method == "euler":
            self.write_euler_method()
        elif self.numerical_method == "runge-kutta-4":
            self.write_runge_kutta_4_method()

        self.write_main()
        self.plot_results()

    def write_head_file(self):
        #Añadimos los imports necesarios.
        self.file.write("import numpy as np\n")
        self.file.write("import matplotlib.pyplot as plt\n")
        self.file.write("import sympy as sp\n")
        self.file.write("\n\n")

    def write_model_parameters(self):
        
        #Añadimos una constante que contenga el número de ecuaciones.
        self.file.write("n_equations = " + str(len(self.equations)) + "\n")

        #Añadimos las constantes de las ecuaciones y sus valores.
        self.file.write("# Parámetros del modelo\n")
        for equation in self.equations:
            constant_values = equation.get_constants_values()
            for constant in equation.get_constants():
                value = constant_values[str(constant)]  # Convertimos la constante a string si es necesario
                self.file.write(f"{constant} = {value}\n")
        self.file.write("\n\n")

        # Añadimos la variable que cuenta los pasos de tiempo
        self.file.write("iteration = 0\n")
        # Crear una lista basada en el número de ecuaciones
        n = len(self.equations[0].get_simbol())
        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

        self.file.write("est = " + list_str + "\n")
        self.file.write("\n\n")

        #Añadimos las constantes de inicio y fin de la simulación.
        self.file.write("t0 = 0\n")
        self.file.write("tf = 50\n")
        self.file.write("dt = 0.1\n")
        self.file.write("t = np.arange(t0, tf, dt)\n")
        self.file.write("\n\n")

    def write_initialization_method(self):
        self.file.write("def initialize():\n")
        self.file.write("    iteration = 0\n")
        # Crear una lista basada en el número de ecuaciones
        n = len(self.equations[0].get_simbol())
        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

        self.file.write("est = " + list_str + "\n")
        self.file.write("f = " + list_str + "\n")
        self.file.write("\n\n")


    def write_equations(self):
        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        self.file.write("def deriv(inp):\n")
        
        #Añadimos la salida del método deriv.
        self.file.write("\tout = []\n")

        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            #Sustituimos los simbolos por la cadena est[i] para poder evaluar la ecuación.

            symbols = equation.get_simbol()
            subs_dict = {str(sym): sp.Symbol(f'inp[{j}]') for j, sym in enumerate(symbols)}
 
            # Realizamos la sustitución con el diccionario generado
            eq = equation.get_equation().subs(subs_dict)
            self.file.write(f"\tout.append({eq})\n")
        self.file.write("\n")

        #Añadimos la salida de la función deriv.
        self.file.write("\treturn out\n")
        self.file.write("\n\n")


    def write_euler_method(self):

        # Añadimos el metodo de Euler para resolver las ecuaciones.
        self.file.write("def one_step_euler(tt, hh, paso):\n")
        self.file.write("    inp = [est[i][paso-1] for i in range(n_equations)]\n")
        self.file.write("    out=deriv(inp)\n")
        self.file.write("    for i in range(n_equations):\n")
        self.file.write("        est[i].append(inp[i] + (hh * out[i]))\n")
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



    def write_main(self):
        self.file.write("def main():\n")
        self.file.write("\tglobal iteration\n")
        
        #Añadimos las condiciones iniciales.
        for i, symbol in enumerate(self.initial_state):
            self.file.write(f"\test[{i}].append({self.initial_state[symbol]})\n")
        
        self.file.write("\n\tfor i in range(1, len(t)):\n")
        self.file.write("\t\titeration += 1\n")
        
        if self.numerical_method == "euler":
            self.file.write("\t\tone_step_euler(t[i-1], dt, iteration)\n")
        elif self.numerical_method == "runge-kutta-4":
            self.file.write("\t\tone_step_runge_kutta_4(t[i-1], dt, iteration)\n")

        self.file.write("\n\n")

    def plot_results(self):
        self.file.write("if __name__ == '__main__':\n")
        self.file.write("    main()\n")

        for i, symbol in enumerate(self.equations[0].get_simbol()):
            self.file.write(f"    plt.plot(t, est[{i}], label='{symbol}')\n")

        self.file.write("    plt.show()\n")
        self.file.write("\n\n")
    
    
eq = Equation()
eq.add_equation("a*x-b*x*y", 'x y', 'a b ', {"a": 5, "b": 0.05})
eq.process_equations()
eq2 = Equation()
eq2.add_equation("c*x*y-d*y", 'x y', 'c d', {"c":0.0004 , "d":0.2})
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], {"x":450,"y":90},"simulation", "runge-kutta-4").generate_file()



    