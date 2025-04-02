from ContinuousModelGenerator import Equation, PythonSimulationGenerator


# Example Pendulum with arguments
eq = Equation("y_1", "y_2", "y_2", {})
eq1 = Equation("y_2", "-(g/l)*sin(y_1)", "y_1", {"g": 9.81, "l": 9.8})

equations = [eq,eq1]
PythonSimulationGenerator(equations, [], {"y_1": 0.541052, "y_2": 0}, [0,40,0.1], "pendulum","plot" ,"runge-kutta-4").generate_file()