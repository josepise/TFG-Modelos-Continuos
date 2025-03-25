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

class PythonSimulationGenerator(SimulationModelGenerator):
    def __init__(self, equations, conditionals, name_file):
        super().__init__(equations, conditionals, name_file)
    
    def generate_file(self):
        # Creamos el archivo de simulación continua en python en la carpeta ../models/name_file.py.
        os.makedirs("./models/", exist_ok=True)
        self.file = open(f"./models/{self.name_file}.py", "w")

        # Escribimos el archivo.
        self.write_head_file()
        self.write_model_parameters()
        self.write_equations()
        self.write_numerical_methods()
        self.write_main()
        self.file.close()

    def write_head_file(self):
        # Añadimos los imports necesarios.
        self.file.write("import numpy as np\n")
        self.file.write("import matplotlib.pyplot as plt\n")
        self.file.write("import sympy as sp\n")
        self.file.write("\n\n")

    def write_model_parameters(self):
        # Añadimos las constantes de las ecuaciones y sus valores.
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

        # Añadimos las constantes de inicio y fin de la simulación.
        self.file.write("t0 = 0\n")
        self.file.write("tf = 10\n")
        self.file.write("dt = 0.01\n")
        self.file.write("\n\n")

    def write_equations(self):
        # Escribimos la cabecera de la función que contendrá las ecuaciones.
        self.file.write("def deriv(t):\n")
        self.file.write("    global i\n")
        self.file.write("    if i == 0:\n")
        self.file.write("        est[0].append(0)\n")
        self.file.write("        est[1].append(0)\n")
        self.file.write("    else:\n")

        # Añadimos las ecuaciones al archivo.
        for i, equation in enumerate(self.equations):
            # Sustituimos los símbolos por la cadena est[i] para poder evaluar la ecuación.
            symbols = equation.get_simbol()
            subs_dict = {str(sym): sp.Symbol(f'est[{j}][i-1]') for j, sym in enumerate(symbols)}
            # Realizamos la sustitución con el diccionario generado
            eq = equation.get_equation().subs(subs_dict)
            self.file.write(f"        est[{i}].append({eq})\n")
        self.file.write("    i += 1\n")
        self.file.write("    return [est[0][-1], est[1][-1]]\n")
        self.file.write("\n")

    def write_numerical_methods(self):
        # Añadimos el método de Euler para resolver las ecuaciones.
        self.file.write("def one_step_euler(inp, tt, hh):\n")
        self.file.write("    f = deriv(tt)\n")
        self.file.write("    out = [0] * len(inp)\n")
        self.file.write("    for j in range(len(inp)):\n")
        self.file.write("        out[j] = inp[j] + (hh * f[j])\n")
        self.file.write("    return out\n")
        self.file.write("\n\n")

    def write_main(self):
        self.file.write("def main():\n")
        self.file.write("    t = np.arange(t0, tf, dt)\n")
        self.file.write("    x = np.zeros((len(t), 2))\n")
        self.file.write("    x[0] = [0, 0]  # Initial conditions\n")
        self.file.write("\n\n")
        self.file.write("    for i in range(1, len(t)):\n")
        self.file.write("        x[i] = one_step_euler(x[i-1], t[i-1], dt)\n")
        self.file.write("\n\n")
        self.file.write("    return t, x\n")
        self.file.write("\n\n")
        self.file.write("if __name__ == '__main__':\n")
        self.file.write("    t, x = main()\n")
        self.file.write("    plt.plot(t, x[:, 0], label='x')\n")
        self.file.write("    plt.plot(t, x[:, 1], label='y')\n")
        self.file.write("    plt.xlabel('Time')\n")
        self.file.write("    plt.ylabel('Values')\n")
        self.file.write("    plt.legend()\n")
        self.file.write("    plt.show()\n")

# Ejemplo de uso
eq = Equation()
eq.add_equation("a*x-b*x*y", 'x y', 'a b ', {"a": 5, "b": 0.2})
eq.process_equations()
eq2 = Equation()
eq2.add_equation("c*x*y-d*y", 'x y', 'c d', {"c":0.05, "d":0.0004})
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], "simulation").generate_file()