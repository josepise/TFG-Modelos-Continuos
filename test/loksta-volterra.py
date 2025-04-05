from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator


# EJEMPLO LOksta-Volterra  
eq = Equation("x","a*x-b*x*y", "x y", {"a": 5, "b": 0.05})
eq2 = Equation("y","c*x*y-d*y", "x y", {"c":0.0004 , "d":0.2})
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], {"y":90,"x":30},[0,50,0.1],"loksta-volterra","csv", "runge-kutta-fehlberg").generate_file()

CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra", "runge-kutta-fehlberg").generate_file()