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
    __init__(equation, simbols, constants, values={}):
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
        self.name = '' # Nombre de la ecuación.
        self.text_equation = [] # Almacena el texto introducido por el usuario de las ecuaciones.
        self.equation = '' # Almacena las ecuaciones procesadas para ser tratadas por sympy.
        self.simbol = '' # Almacena los símbolos de la ecuación.
        self.constant_values = {} # Diccionario para almacenar los valores de las constantes de las ecuaciones.

    def __init__(self, name, equation, simbols, constant_values={}):
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
        self.text_equation = [] # Almacena el texto introducido por el usuario de las ecuaciones.
        self.constant_values = {} # Diccionario para almacenar los valores de las constantes de las ecuaciones.

        if equation:
            self.name = name
            self.text_equation.append(equation)
            self.text_equation.append(simbols)
            self.constant_values.update(constant_values)
            self.process_equations()
          
    def get_name(self):
        """Devuelve el nombre de la ecuación."""
        return self.name
    
    def get_equation(self):
        """Devuelve la ecuación procesada."""
        return self.equation
    
    def get_constants(self):
        """Devuelve las constantes de la ecuación."""
        return self.constant_values.keys()
    
    def get_constants_values(self):
        """Devuelve el diccionario de constantes con sus valores."""        
        return self.constant_values
    
    
    def get_symbol(self):
        """Devuelve los símbolos de la ecuación."""
        if type(self.simbol) == sp.Symbol:
            self.simbol = [self.simbol]

        return self.simbol

    def process_equations(self):
        """
        Convierte el texto de las ecuaciones, símbolos y constantes en objetos sympy y los almacena en los atributos correspondientes.
        Returns:
            str: Una cadena de texto que contiene los errores encontrados durante el procesamiento de las ecuaciones, símbolos y constantes.
            Si no hay errores, la cadena estará vacía.
        Errores posibles:
            - "Error(Wrong Equation): La ecuación no es válida."
            - "Error(Wrong Symbols): Los símbolos no son válidos."
            - "Error(Wrong Constants): Las constantes no son válidas."
        Excepciones:
            - Cualquier excepción generada durante la conversión de texto a objetos sympy será capturada y el mensaje de error correspondiente
              se agregará a la cadena de errores.
        """
       
        errors = ""      
        try:
            self.equation=sp.sympify(self.text_equation[0])
        except:
            errors += "Error(Wrong Equation): La ecuación no es válida."
        
        try:
            self.simbol = sp.symbols(self.text_equation[1])
        except:
            errors += f"\nError(Wrong Symbols): Los símbolos no son válidos."

        try:
            self.constants = sp.symbols(self.constant_values.keys(), constant=True)
        except:
            errors += f"\nError(Wrong Constants): Las constantes no son válidas."
       

        return errors
    
    def check_components(self):
        """
        Verifica que los componentes de la ecuación sean correctos y estén presentes.
        Este método realiza varias comprobaciones en la ecuación almacenada en el objeto:
        1. Verifica que todos los símbolos especificados estén presentes en la ecuación.
        2. Verifica que todas las constantes especificadas estén presentes en la ecuación.
        3. Verifica que todas las constantes tengan un valor asignado.
        4. Intenta sustituir las constantes en la ecuación con sus valores correspondientes.
        Returns:
            str: Una cadena de texto que contiene los errores encontrados durante las comprobaciones.
                 Si no se encuentran errores, la cadena estará vacía.
        Errores posibles:
            - Error(Missing Symbol): Indica que un símbolo especificado no se encuentra en la ecuación.
            - Error(Missing Constant): Indica que una constante especificada no se encuentra en la ecuación.
            - Error(Missing Constant Value): Indica que una constante especificada no tiene un valor asignado.
            - Error(Wrong Constants Values): Indica que los valores de las constantes no son válidos para la sustitución en la ecuación.
        """
        errors = ""

        # Convertimos free_symbols a un conjunto de strings para facilitar la comparación
        equation_symbols = {str(symbol) for symbol in self.equation.free_symbols}

        # Comprobamos que los símbolos se encuentren en la ecuación
        for s in self.simbol:
            if str(s) not in equation_symbols:
                errors += f"\nError(Missing Symbol): El símbolo {s} no se encuentra en la ecuación."
        

        # Comprobamos que las constantes se encuentren en la ecuación
        for c in self.constants_values.keys():
            if str(c) not in equation_symbols:
                errors += f"\nError(Missing Constant): La constante {c} no se encuentra en la ecuación."
        

        try:
            self.equation = self.equation.subs(self.constant_values)
        except:
            errors += f"\nError(Wrong Constants Values): Los valores de las constantes no son válidos."

        return errors
    
