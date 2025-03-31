from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator


# EJEMPLO LOksta-Volterra  
eq = Equation()
eq.add_equation("x","a*x-b*x*y", "x y", "a b", {"a": 5, "b": 0.05})
eq.process_equations()
eq2 = Equation()
eq2.add_equation("y","c*x*y-d*y", "x y", "c d", {"c":0.0004 , "d":0.2})
eq2.process_equations()
equations = [eq, eq2]

# PythonSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra","csv", "runge-kutta-4").generate_file()

CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra",  "runge-kutta-4").generate_file()