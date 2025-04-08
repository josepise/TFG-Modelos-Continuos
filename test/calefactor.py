from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator
from ContinuousModelGenerator import Condition
import sympy as sp

# EJEMPLO Calefactor Diapositivas Tema 6
eq= Equation("v_w", "(k/T)*p*u_t-(1/T)*v_w", "v_w", {"k": 1, "T": 7, "p": 10, "u_t": 1})

cond=Condition(["vr-(v_w+v_e)<-s"],["u_t=0"],"v_w",{"s":0.8,"vr":20,"v_e":15})
cond1=Condition(["vr-(v_w+v_e)>s"],["u_t=1"],"v_w",{"s":0.8,"vr":20,"v_e":15})
PythonSimulationGenerator([eq], [cond,cond1], {"v_w":0},[0,50,0.2],"calefactor","plot", "runge-kutta-fehlberg").generate_file()

# CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra",  "runge-kutta-4").generate_file()