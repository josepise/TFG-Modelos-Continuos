from abc import ABC, abstractmethod
from equation import Equation
import sympy as sp
import os

class SimulationModelGenerator(ABC):
    

    def __init__(self, equations, conditionals, name_file):
        self.equations = equations
        self.conditionals = conditionals
        self.name_file = name_file
    
    @abstractmethod
    def generate_file(self):
        pass


    #def check_components(self):
        

# Hacemos una clase que genere el archivo de simulación continua en python.

class PythonSimulationGenerator(SimulationModelGenerator):

    def __init__(self, equations, conditionals, name_file):
        super().__init__(equations, conditionals, name_file)
    

    def generate_file(self):
        
        #Creamos el archivo de simulación continua en python en la carpeta 
        # ../models/name_file.py.
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.py", "w")

        #Escribimos el archivo.
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()
        self.write_numerical_methods()

    def write_head_file(self):
        #Añadimos los imports necesarios.
        self.file.write("import numpy as np\n")
        self.file.write("import matplotlib.pyplot as plt\n")
        self.file.write("import sympy as sp\n")
        self.file.write("\n\n")

    def write_model_parameters(self):
        
        #Añadimos las constantes de las ecuaciones y sus valores.
        self.file.write("# Parámetros del modelo\n")
        for equation in self.equations:
            constant_values = equation.get_constants_values()
            for constant in equation.get_constants():
                value = constant_values[str(constant)]  # Convertimos la constante a string si es necesario
                self.file.write(f"{constant} = {value}\n")
        self.file.write("\n\n")

        # Añadimos la variable que cuenta los pasos de tiempo
        self.file.write("i = 0\n")
        # Crear una lista basada en el número de ecuaciones
        n = len(self.equations[0].get_simbol())
        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

    
        self.file.write("est = " + list_str + "\n")
        self.file.write("\n\n")

        #Añadimos las constantes de inicio y fin de la simulación.
        self.file.write("t0 = 0\n")
        self.file.write("tf = 10\n")
        self.file.write("dt = 0.01\n")
        self.file.write("\n\n")

    def write_initialization_method(self):
        self.file.write("def initialize():\n")
        self.file.write("    i = 0\n")
        self.file.write("    est = [[], []]\n")
        self.file.write("\n\n")


    def write_equations(self):

        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        self.file.write("def deriv(t):\n")

        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            #Sustituimos los simbolos por la cadena est[i] para poder evaluar la ecuación.

            symbols = equation.get_simbol()
            subs_dict = {str(sym): sp.Symbol(f'est[{j}][i]') for j, sym in enumerate(symbols)}
 
            # Realizamos la sustitución con el diccionario generado
            eq = equation.get_equation().subs(subs_dict)
            self.file.write(f"\test[{i}].append({eq})\n")
        self.file.write("\n")


    def write_numerical_methods(self):

        #Añadimos el metodo de Euler para resolver las ecuaciones.
        self.file.write("def one_step_euler(inp, tt, hh):\n")
        self.file.write("    f = deriv(tt)\n")
        self.file.write("    out = [0] * len(inp)\n")
        self.file.write("    for i in range(len(inp)):\n")
        self.file.write("        out[i] = inp[i] + (hh * f[i])\n")
        self.file.write("    return out\n")
        self.file.write("\n\n")

    def write_main(self):
        self.file.write("def main():\n")
        self.file.write("    t = np.arange(t0, tf, dt)\n")
        self.file.write("    x = np.zeros((len(t), 1))\n")
        self.file.write("    x[0] = x0\n")
        self.file.write("\n\n")
        self.file.write("    for i in range(1, len(t)):\n")
        self.file.write("        x[i] = one_step_euler(x[i-1], t[i-1], dt)\n")
        self.file.write("\n\n")
        self.file.write("    return t, x\n")
        self.file.write("\n\n")
    
    
eq=Equation()    
eq.add_equation("a*x**2 + b*x + c*y", 'x y', 'a b c', {"a": 1, "b": 2, "c": 3})
eq.process_equations()
eq2=Equation()
eq2.add_equation("d*x**2 + e*x + f*y", 'x y', 'd e f', {"d": 4, "e": 5, "f": 6})
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], "simulation").generate_file()



    