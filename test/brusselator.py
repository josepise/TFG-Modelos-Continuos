from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator


# EJEMPLO The Brusselator pag 359 
eq = Equation()
eq.add_equation("x","a-(b+1)*x+x^2*y", "x y", "a b", {"a": 1, "b": 3})
eq.process_equations()
eq2 = Equation()
eq2.add_equation("y","b*x-x^2*y", "x y", "b", {"b":3 })
eq2.process_equations()
equations = [eq, eq2]

PythonSimulationGenerator(equations, [], {"x":2,"y":1},[0,50,0.2],"brusselator","plot", "runge-kutta-4").generate_file()

# CppSimulationGenerator(equations, [], {"x":30,"y":90},[0,50,0.1],"loksta-volterra",  "runge-kutta-4").generate_file()