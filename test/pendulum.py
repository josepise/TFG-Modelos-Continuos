from ContinuousModelGenerator import Equation, PythonSimulationGenerator


# Ejemplo Pendulo
eq=Equation()
eq.add_equation("y_1","y_2","y_2","",{})
eq.process_equations()

eq1=Equation()
eq1.add_equation("y_2","-(g/l)*sin(y_1)","y_1","g l",{"g":9.8,"l":10})
eq1.process_equations()

equations = [eq,eq1]
PythonSimulationGenerator(equations, [], {"y_1": 3.1, "y_2": 0}, [0,10,0.1], "pendulum", "runge-kutta-4").generate_file()