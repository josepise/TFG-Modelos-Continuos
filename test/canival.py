from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator

# Ejemplo canival 
eq=Equation()
eq.add_equation("p_1","a*p_4-p_1-p_1*p_2","p_1 p_2 p_4","a",{"a":2})
eq.process_equations()

eq1=Equation()
eq1.add_equation("p_2","p_1-p_2-p_2*p_3","p_1 p_2 p_3","",{})
eq1.process_equations()

eq2=Equation()
eq2.add_equation("p_3","p_2-p_3-p_3*p_4","p_2 p_3 p_4","",{})
eq2.process_equations()

eq3=Equation()
eq3.add_equation("p_4","p_3-p_4","p_3 p_4","",{})
eq3.process_equations()

equations = [eq,eq1,eq2,eq3]

PythonSimulationGenerator(equations, [], {"p_1": 1, "p_2": 0, "p_3": 0, "p_4": 0}, [0,10,0.1], "canivals","plot", "runge-kutta-4").generate_file()

# CppSimulationGenerator(equations, [], {"p_1": 1, "p_2": 0, "p_3": 0, "p_4": 0}, [0,10,0.1], "canivals","csv", "runge-kutta-4").generate_file()