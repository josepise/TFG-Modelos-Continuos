import sympy as sp
from .equation import Equation

class Condition:

    def __init__(self):
        #Inicializamos los valores de la condición.
        self.left_value = ""                # Pueden ser número o Equations.
        self.right_value = ""               # Pueden ser número o Equations.
        self.avaliable_operators = ["<", "<=", ">", ">=", "==", "!="] # Lista de operadores disponibles.
        self.selected_operator = ""           # Este objeto siempre será un string.

    def add_condition(self, left_condition, right_text_condition, selected_operator):
        self.left_condition = left_condition                # Este objeto siempre será una expresión de SymPy.
        self.right_condition = right_text_condition         # Este objeto puede ser o un número o una expresión de SymPy.
        self.selected_operator = selected_operator                          # Este objeto siempre será un string.


    def get_available_operators(self):  
        #Devuelve la lista de operadores disponibles.
        return self.avaliable_operators

    def check_condition(self):
        
        #Comprobamos que left_condition sea una expresión de SymPy.
        if not isinstance(self.left_condition, sp.Expr):
            return f"Error(Wrong Condition): El valor de la condición izquierda no es una expresión de SymPy.\n \
                    Valor introducido: {self.left_condition}"

        #Comprobamos que right_condition sea un número o una expresión de SymPy.
        if not isinstance(self.right_condition, (int, float, sp.Expr)):
            return f"Error(Wrong Condition): El valor de la condición derecha no es un número ni una expresión de SymPy.\n \
                    Valor introducido: {self.right_condition}"
    

    def show_condition(self):
        #Devuelve la condición en forma de string utilizando la función sp.latex().
        #Mirar notas sobre como devolver este campo.

        return sp.latex(self.left_condition) + self.operator + sp.latex(self.right_condition)
    