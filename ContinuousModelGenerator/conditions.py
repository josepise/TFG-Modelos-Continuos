import sympy as sp
from .equation import Equation

class Condition:
    
    def __init__(self, text_equation, text_result, text_variables, constants):
        #Inicializamos los valores de la condición.
        self.text_condition = [text_equation,text_variables, text_result]  # Lista de expresiones que definen la condición.
        self.avaliable_operators = ["<", "<=", ">", ">=", "==", "!="]      # Lista de operadores disponibles.
        self.constants = constants                                         # Este objeto siempre será un diccionario en el  que las claves son los nombres de las variables
                                                                           # y los valores son los valores de las variables.
        self.variables = None                                              # Lista de variables que forman parte de la condición.
        self.result = [None] * len(text_result)                            # Lista de expresiones que se aplicaran cuando se cumpla la condición.
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
        if type(self.variables) == sp.Symbol:
            self.variables = [self.variables]
            
        return self.variables
    
    def get_text_symbols(self):
        #Devuelve la lista de símbolos de la condición en forma de string.
        if type(self.variables) == list:
            text=[str(sym) for sym in self.variables]
        else:
            text=[str(self.variables)]
        return " ".join(text).replace(" ", ",")
    
    def get_conditions(self):
        #Devuelve la lista de condiciones.
        return self.conditions
    
    def get_text_condition(self):
        #Devuelve la lista de condiciones en forma de string.
        return ", ".join(self.text_condition[0])
    
    def get_result(self):
        #Devuelve la lista de resultados.
        return  self.result
    
    def get_text_result(self):
        #Devuelve la lista de resultados en forma de string.
        return ", ".join(self.text_condition[2])

    def get_results_var(self):
        #Devuelve la lista de variables que modifican su valor.
        print(self.result)
        return [self.result[i][0].lhs for i in range(len(self.result))]

    def get_constants(self):
        #Devuelve el diccionario de constantes.
        return self.constants.keys()
    
    def get_text_constants(self):
        #Devuelve el diccionario de constantes en forma de string.
        text=[f"{key}={value}" for key, value in self.constants.items()]
        return ",".join(text)
    
    def get_constants_values(self):
        #Devuelve el diccionario de constantes.
        return self.constants
    
    def show_condition(self):
        #Devuelve la condición en forma de string utilizando la función sp.latex().
     
        return [sp.latex(self.conditions[i]) for i in range(len(self.conditions))]
    
    def check_components(self):
        
        cond_symbols=[]
        for con in self.conditions:
            #Comprobamos si la condición es válida.
            operators=[op for op in self.avaliable_operators if op in str(con)]

            if  len(operators) == 0:
                return ("INVALID_INPUT_COND_EXP", ",".join(self.avaliable_operators))

            elif len(operators) > 1:
                op_str= ",".join(operators)

                #Si hay más de un operador, mostramos un mensaje de error.
                return ("INVALID_INPUT_COND_MULTIPLE_OP",op_str)
            
            cond_symbols += [str(symbol) for symbol in con.free_symbols]
            
        cond_symbols = list(set(cond_symbols))
            


        # Comprobamos que los símbolos se encuentren en las expresiones de la condición
        for s in self.get_symbols():
            if str(s) not in cond_symbols:
                return ("INVALID_COND_VAR_NOT_APPEAR", s)
        

        # Comprobamos que las constantes se encuentren en las expresiones de la condición
        for c in self.constants.keys():
            if str(c) not in cond_symbols:
                return ("INVALID_COND_CONSTANT_NOT_APPEAR", c)
            
        # Comprobamos que no queden simbolos libres en la ecuación
        str_symbols={str(symbol) for symbol in self.variables}

        for s in cond_symbols:
            # Si el símbolo está en la ecuación y no es una variable/constante, lo consideramos un error
            if s not in str_symbols and s not in self.constants.keys():
                return ("INVALID_COND_FREE_SYMBS", s)    
            
        # Comprobamos que no haya simbolos iguales como variables y constantes
        symbols = list(self.variables)+list(self.constants.keys())
        var_const = set({str(symbol) for symbol in symbols})

        for s in var_const:
            if s in self.constants.keys() and s in str_symbols:
                return ("INVALID_COND_DUP_SYMBS", s)

            
        return (None, None)
        