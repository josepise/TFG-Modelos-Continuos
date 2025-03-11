import sympy as sp

class Equation:
    """
    Equation es una clase que representa una ecuación que puede ser procesada y resuelta.
    Atributos
    ---------
    text_equation : list
        Almacena el texto introducido por el usuario de las ecuaciones.
    equation : sympy.Expr
        Almacena las ecuaciones procesadas para ser tratadas por sympy.
    simbol : sympy.Symbol
        Almacena los símbolos de la ecuación.
    constants : sympy.Symbol
        Almacena las constantes de la ecuación.
    constant_values : dict
        Diccionario para almacenar los valores de las constantes de la ecuación.
    
    Métodos
    -------
    __init__():
        Inicializa la clase Equation con listas vacías para almacenar la ecuación y un diccionario para los valores de las constantes.
    add_equation(equation, simbols, constants, values={}):
        Agrega una ecuación, sus símbolos y constantes.
    get_equation():
        Retorna la ecuación procesada.
    get_constants_values():
        Retorna el diccionario de constantes con sus valores.
    get_simbol():
        Retorna los símbolos de la ecuación.
    process_equations():
        Convierte el texto de la ecuación, símbolos y constantes en objetos sympy y los almacena.
    """
    def __init__(self):
        self.text_equation = [] # Almacena el texto introducido por el usuario de las ecuaciones.
        self.equation = '' # Almacena las ecuaciones procesadas para ser tratadas por sympy.
        self.simbol = '' # Almacena los símbolos de la ecuación.
        self.constants = '' # Almacena las constantes de la ecuación.
        self.constant_values = {} # Diccionario para almacenar los valores de las constantes de las ecuaciones.

    def add_equation(self, equation, simbols, constants, values={}):
        """ 
        Método para agregar una ecuación a la lista de ecuaciones.
        Parameters
        ----------
        equation : str
            Cadena de texto con la ecuación.
        simbols : str
            Cadena de texto con los símbolos de la ecuación.
        constants : str
            Cadena de texto con las constantes de la ecuación.
        values : dict, optional
            Diccionario con los valores de las constantes.
        """
        if equation:
            self.text_equation.append(equation)
            self.text_equation.append(simbols)
            self.text_equation.append(constants)
            self.constant_values.update(values)
    
    def get_equation(self):
        """Devuelve la ecuación procesada."""
        return self.equation
    
    def get_constants_values(self):
        """Retorna el diccionario de constantes con sus valores."""
        return self.constant_values
    
    def get_simbol(self):
        """Retorna los símbolos de la ecuación."""
        return self.simbol

    def process_equations(self):
        """Convierte el texto de las ecuaciones, símbolos y constantes en objetos sympy y los almacena en los atributos correspondientes."""       
        self.equation = sp.sympify(self.text_equation[0])
        self.simbol = sp.symbols(self.text_equation[1])
        self.constants = sp.symbols(self.text_equation[2], constant=True)
        self.equation = self.equation.subs(self.constant_values)
