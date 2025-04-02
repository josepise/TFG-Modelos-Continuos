from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator


# EJEMPLO Descomposicion de moleculas pag 351  
eq = Equation()
eq.add_equation("a","-k*a*a+r*a*b", "a b", "k r", {"k": 0.2, "r": 0.1})
eq.process_equations()
eq2 = Equation()
eq2.add_equation("b","k*a*a-r*a*b-d*b", "a b", "k r d", {"k":0.2 , "r":0.1, "d":0})
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], {"a":1,"b":0},[0,50,0.1],"descomposition_molecule","plot", "runge-kutta-4").generate_file()

# CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra",  "runge-kutta-4").generate_file()