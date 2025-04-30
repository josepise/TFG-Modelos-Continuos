from ContinuousModelGenerator import PythonSimulationGenerator, Equation, CppSimulationGenerator, JavaSimulationGenerator

# Ejemplo canival 
eq=Equation("p_1","a*p_4-p_1-p_1*p_2","p_1 p_2 p_4",{"a":2})
eq1=Equation("p_2","p_1-p_2-p_2*p_3","p_1 p_2 p_3",{})
eq2=Equation("p_3","p_2-p_3-p_3*p_4","p_2 p_3 p_4",{})
eq3=Equation("p_4","p_3-p_4","p_3 p_4",{})


equations = [eq,eq1,eq2,eq3]

PythonSimulationGenerator(equations, [], {"p_1": 1, "p_2": 0, "p_3": 0, "p_4": 0}, [0,10,0.1],"/mnt/c/Users/jose/Documents/GitHub/TFG-Modelos-Continuos/models", "canivals-euler","plot", "runge-kutta-fehlberg").generate_file()
# JavaSimulationGenerator(equations, [], {"p_1": 1, "p_2": 0, "p_3": 0, "p_4": 0}, [0,10,0.1], "canivals", "runge-kutta-fehlberg").generate_file()
# PythonSimulationGenerator(equations, [], {"p_1": 1, "p_2": 0, "p_3": 0, "p_4": 0}, [0,10,0.1], "canivals-runge","csv", "runge-kutta-4").generate_file()

# CppSimulationGenerator(equations, [], {"p_1": 1.0, "p_2": 0.0, "p_3": 0.0, "p_4": 0.0}, [0,10,0.1], "canivals", "runge-kutta-fehlberg").generate_file()