from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator


# EJEMPLO Descomposicion de moleculas pag 351  
eq = Equation("a","-k*a**2+r*a*b", "a b", {"k": 0.2, "r": 0.1})
eq2 = Equation("b","k*a**2-r*a*b-d*b", "a b", {"k":0.2 , "r":0.1, "d":0})

equations = [eq, eq2]

PythonSimulationGenerator(equations, [], {"a":1,"b":0},[0,50,0.1],"descomposition_molecule","plot", "runge-kutta-fehlberg").generate_file()

# JavaSimulationGenerator(equations, [], {"a":1,"b":0},[0,50,0.1],"descomposition_molecule", "runge-kutta-fehlberg").generate_file()

# CppSimulationGenerator(equations, [], {"a":1,"b":0},[0,50,0.1],"descomposition_molecule",  "runge-kutta-fehlberg").generate_file()