from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator
from ContinuousModelGenerator import Condition
import sympy as sp

# EJEMPLO Calefactor Diapositivas Tema 6
eq= Equation("v_w", "(k/T)*p-(1/T)*v_w", "v_w", {"k": 1, "T": 1, "p": 0})

cond=Condition(sp.Symbol("p"), 0, "<=")

PythonSimulationGenerator([eq], [], {"v_w":0},[0,50,0.2],"brusselator","plot", "runge-kutta-4").generate_file()

# CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra",  "runge-kutta-4").generate_file()