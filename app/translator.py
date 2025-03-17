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

        import os
        os.makedirs("./models/", exist_ok=True)
        file = open(f"./models/{self.name_file}.py", "w")

        #Añadimos los imports necesarios.
        file.write("import numpy as np\n")
        file.write("import matplotlib.pyplot as plt\n")
        file.write("import sympy as sp\n")
        file.write("\n\n")

        #Añadimos las constantes de las ecuaciones y sus valores.
        file.write("# Parámetros del modelo\n")
        for equation in self.equations:
            constant_values = equation.get_constants_values()
            for constant in equation.get_constants():
                value = constant_values[str(constant)]  # Convertimos la constante a string si es necesario
                file.write(f"{constant} = {value}\n")
        file.write("\n\n")

        # Suponiendo que quieres crear una lista basada en el número de ecuaciones
        n = len(self.equations[0].get_simbol())
        list_str = f"[{', '.join(['[]' for _ in range(n)])}]"

        # Para usarlo en tu código actual:
        file.write("est = " + list_str + "\n")
        file.write("\n\n")

        #Añadimos las constantes de inicio y fin de la simulación.
        file.write("t0 = 0\n")
        file.write("tf = 10\n")
        file.write("dt = 0.01\n")
        file.write("\n\n")
      
        #Escribimos la cabecera de la función que contendrá las ecuaciones.
        file.write("def deriv(t):\n")

        #Añadimos las ecuaciones al archivo.
        for i,equation in enumerate(self.equations):
            #Sustituimos los simbolos por la cadena est[i] para poder evaluar la ecuación.

            symbols = equation.get_simbol()
            subs_dict = {str(sym): sp.Symbol(f'est[{j}]') for j, sym in enumerate(symbols)}
 
            # Realizamos la sustitución con el diccionario generado
            eq = equation.get_equation().subs(subs_dict)
            file.write(f"\teq[{i}].append({eq})\n")
        file.write("\n")

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
    
    
eq=Equation()    
eq.add_equation("a*x**2 + b*x + c*y", 'x y', 'a b c', {"a": 1, "b": 2, "c": 3})
eq.process_equations()
eq2=Equation()
eq2.add_equation("d*x**2 + e*x + f*y", 'x y', 'd e f', {"d": 4, "e": 5, "f": 6})
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], "simulation").generate_file()



    