from ContinuousModelGenerator import Equation, PythonSimulationGenerator


# Ejemplo Pendulo con muelle (pag. 346)
eq=Equation()
eq.add_equation("y_1","y_2","y_2","",{})
eq.process_equations()

eq1=Equation()
eq1.add_equation("y_2","y_1*y_4*y_4+g*cos(y_3)-k*(y_1-l_0)","y_1 y_4 y_3","g l_0 k",{"g":1,"l_0":1,"k":1})
eq1.process_equations()

eq2=Equation()
eq2.add_equation("y_3","y_4","y_4","",{})
eq2.process_equations()

eq3=Equation()
eq3.add_equation("y_4","-2*(y_2*y_4)/y_1-g*(sin(y_3)/y_1)","y_1 y_2 y_3 y_4","",{})
eq3.process_equations()

equations = [eq,eq1,eq2,eq3]
PythonSimulationGenerator(equations, [], {"y_1":3.1, "y_2": 0,"y_3" :0 ,"y_4":0} , [0,40,0.1], "spring-pendulum", "runge-kutta-4").generate_file()