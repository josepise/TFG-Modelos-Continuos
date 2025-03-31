import sympy as sp

class Condition:

    def __init__(self):
        #Inicializamos los valores de la condición.
        self.left_value = ""
        self.right_value = ""
        self.operator= ""

    def add_condition(self, left_condition, right_text_condition, operator):
        self.left_condition = left_condition                # Este objeto siempre será una expresión de SymPy.
        self.right_condition = right_text_condition         # Este objeto puede ser o un número o una expresión de SymPy.
        self.operator = operator                            # Este objeto siempre será un string.


    def check_condition(self):
        
        #Comprobamos que left_condition sea una expresión de SymPy.
        if not isinstance(self.left_condition, sp.Expr):
            return "Error(Wrong Condition): El valor de la condición izquierda no es una expresión de SymPy."

        #Comprobamos que right_condition sea un número o una expresión de SymPy.
        if not isinstance(self.right_condition, (int, float, sp.Expr)):
            return "Error(Wrong Condition): El valor de la condición derecha no es un número ni una expresión de SymPy."
    

    def show_condition(self):
        #Devuelve la condición en forma de string utilizando la función sp.latex().
        #Mirar notas sobre como devolver este campo.

        return sp.latex(self.left_condition) + self.operator + sp.latex(self.right_condition)
    