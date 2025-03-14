from abc import ABC, abstractmethod
from equation import Equation
import sympy as sp

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
        # ../models/filename.py.

        file = open(f"../models/{self.name_file}.py", "w")

        #Añadimos los imports necesarios.
        file.write("import numpy as np\n")
        file.write("import matplotlib.pyplot as plt\n")
        file.write("import sympy as sp\n")
        file.write("\n\n")


        #Añadimos las constantes de las ecuaciones y sus valores.
        for equation in self.equations:
            file.write(f"{equation.constants} = {equation.constant_values}\n")
        file.write("\n\n")

        # Suponiendo que quieres crear una lista basada en el número de ecuaciones
        n = len(self.equations)
        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

        # Para usarlo en tu código actual:
        file.write("f = " + list_str + "\n")
        file.write("\n\n")

        #Añadimos las constantes de inicio y fin de la simulación.
        file.write("t0 = 0\n")
        file.write("tf = 10\n")
        file.write("dt = 0.01\n")
        file.write("f =\n")
        file.write("\n\n")
      
        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        file.write("def f(est, t):\n")

        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            #Sustituimos los simbolos por la cadena est[i] para poder evaluar la ecuación.
            eq=equation.get_equation().subs({"x": sp.Symbol('est[1]'), "y": sp.Symbol('est[2]')})
            file.write(f"\tf[{i}].append({equation.equation})\n")

        #Añadimos el metodo de Euler para resolver las ecuaciones.
        file.write("def euler_method():\n")
        file.write("    t = np.arange(t0, tf, dt)\n")
        file.write("    x = np.zeros((len(t), 1))\n")
        file.write("    x[0] = x0\n")
        file.write("\n")
        file.write("    for i in range(1, len(t)):\n")
        file.write("        x[i] = x[i-1] + dt*f(x[i-1], t[i-1])\n")
        file.write("\n")
        file.write("    return t, x\n")
        file.write("\n\n")

    




    