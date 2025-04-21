# Crear manualmente
from ContinuousModelGenerator import Equation, Condition, ContinuousModelGenerator


eq=Equation("p_1","a*p_4-p_1-p_1*p_2","p_1 p_2 p_4",{"a":2})
eq1=Equation("p_2","p_1-p_2-p_2*p_3","p_1 p_2 p_3",{})
eq2=Equation("p_3","p_2-p_3-p_3*p_4","p_2 p_3 p_4",{})
eq3=Equation("p_4","p_3-p_4","p_3 p_4",{})


equations = [eq,eq1,eq2,eq3]

model = ContinuousModelGenerator()
model.equations = equations
model.time_range = [0, 50, 0.2]
model.name = "calefactor"
model.output_format = "csv"
model.method = "runge-kutta-4"

# Guardar
model.save_config(".","calefactor_config.yaml")

# Cargar desde cero
model2 = ContinuousModelGenerator.load_config(".","calefactor_config.yaml")

model2.save_config(".","calefactor_config2.yaml")