import sympy as sp
from .equation import Equation

class Condition:

    def __init__(self):
        #Inicializamos los valores de la condición.
        self.list_text_condition = []                                   # Lista de expresiones que definen la condición.
        self.conditions= []                                             # Lista de objetos de Sympy que definen las condiciones.
        self.avaliable_operators = ["<", "<=", ">", ">=", "==", "!="]   # Lista de operadores disponibles.
        self.result = []                                                # Lista de expresiones que se aplicaran cuando se cumpla la condición.
    
    def __init__(self, text_equation, text_result, text_variables, constants):
        #Inicializamos los valores de la condición.
        self.text_condition = [text_equation,text_variables, text_result]  # Lista de expresiones que definen la condición.
        self.avaliable_operators = ["<", "<=", ">", ">=", "==", "!="]           # Lista de operadores disponibles.
        self.constants = constants                                              # Este objeto siempre será un diccionario en el  que las claves son los nombres de las variables
                                                                                # y los valores son los valores de las variables.
        self.variables = None                                                   # Lista de variables que forman parte de la condición.
        self.result = [None] * len(text_result)                                                      # Lista de expresiones que se aplicaran cuando se cumpla la condición.
        self.conditions = [None] * len(text_equation)                      # Lista de objetos de Sympy que definen las condiciones.

        self.process_condition()                                          # Procesamos la condición
    def add_condition(self, list_text_equation, result, constants):
        #Añadimos una nueva condición a la lista de condiciones.
        self.list_text_condition.append(list_text_equation)               # Añadimos la nueva condición a la lista de condiciones.
        self.constants = constants                                        # Actualizamos el diccionario de constantes.
        self.result.append(result)                                         # Añadimos el resultado a la lista de resultados.
    
    def process_condition(self):
        #Procesamos la condición y la convertimos en una expresión de SymPy.
        for i in range(len(self.text_condition[0])):
            #Convertimos la condición en una expresión de SymPy utilizando el método sympify().
            self.conditions[i] = sp.sympify(self.text_condition[0][i])
   
        #Guardamos las variables que forman parte de la condición.
        self.variables = sp.symbols(self.text_condition[1])

        #Guardamos el resultado de la condición.
        for i in range(len(self.text_condition[2])):
            lhs, rhs = self.text_condition[2][i].split('=')
            self.result[i] = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))


    def get_available_operators(self):  
        #Devuelve la lista de operadores disponibles.
        return self.avaliable_operators

    def get_symbols(self):
        #Devuelve la lista de símbolos de la condición.
        return self.variables
    
    def get_conditions(self):
        #Devuelve la lista de condiciones.
        return self.conditions
    
    def get_result(self):
        #Devuelve la lista de resultados.
        return self.result
    
    def get_results_var(self):
        #Devuelve la lista de variables que modifican su valor.
        return [self.result[i].lhs for i in range(len(self.result))]

    def get_constants(self):
        #Devuelve el diccionario de constantes.
        return self.constants.keys()
    
    def get_constants_values(self):
        #Devuelve el diccionario de constantes.
        return self.constants
    


    def show_condition(self):
        #Devuelve la condición en forma de string utilizando la función sp.latex().
     
        return [sp.latex(self.conditions[i]) for i in range(len(self.conditions))]
    