from .translators import (python_translator, cpp_translator, translator)
from .equation import Equation
from .conditions import Condition


class ContinuousModelGenerator:
    """
    Clase para generar modelos continuos en Python y C++.
    """

    def __init__(self):
        """
        Inicializa el ContinuousModelGenerator con los parámetros dados.

        :param equations: Lista de ecuaciones a procesar.
        :param parameters: Lista de parámetros para las ecuaciones.
        :param initial_conditions: Diccionario de condiciones iniciales.
        :param time_range: Lista que contiene el tiempo inicial, tiempo final y tamaño del paso.
        :param file_name: Nombre del archivo de salida.
        :param translator_type: Tipo de traductor a usar (Python o C++).
        :param method: Método numérico para la simulación (por ejemplo, Runge-Kutta).
        """
        self.equations = []
        self.conditions = []
        self.initial_conditions = None
        self.time_range = None
        self.file_name = None
        self.translator_type = None
        self.method = None
        self.translator = None
        # self.set_translator()

    # Inicializa el traductor apropiado basado en el tipo de traductor
    def set_translator(self):
        if self.translator_type == "python":
            self.translator = python_translator.PythonSimulationGenerator(
                self.equations, self.conditions, self.initial_conditions, self.time_range, 
                self.file_name, self.method
            )
        elif self.translator_type == "cpp":
            self.translator = cpp_translator.CppSimulationGenerator(
                self.equations, self.conditions, self.initial_conditions, self.time_range, 
                self.file_name, self.method
            )
        else:
            raise ValueError("Tipo de traductor inválido. Elija 'python' o 'cpp'.")
            
    def get_equations(self):
        """
        Obtiene las ecuaciones.
        """
        return self.equations
    
    def get_conditions(self):
        """
        Obtiene las condiciones.
        """
        return self.conditions
    
    def get_initial_conditions(self):
        """
        Obtiene las condiciones iniciales.
        """
        return self.initial_conditions
    
    def get_time_range(self):
        """
        Obtiene el rango de tiempo.
        """
        return self.time_range
    
    def get_file_name(self):
        """
        Obtiene el nombre del archivo.
        """
        return self.file_name
    
    def get_translator_type(self):
        """
        Obtiene el tipo de traductor.
        """
        return self.translator_type
    
    def get_method(self):
        """
        Obtiene el método numérico.
        """
        return self.method

    def generate_file(self):
        """
        Genera el archivo de salida.
        """
        self.translator.generate_file()
    
    def set_equations(self, equations):
        """
        Establece las ecuaciones.
        """
        self.equations = equations
        self.translator.set_equations(equations)

    def set_conditions(self, conditions):
        """
        Establece las condiciones.
        """
        self.conditions = conditions
        self.translator.set_conditions(conditions)

    def set_initial_conditions(self, initial_conditions):
        """
        Establece las condiciones iniciales.
        """
        self.initial_conditions = initial_conditions
        self.translator.set_initial_conditions(initial_conditions)

    def set_time_range(self, time_range):
        """
        Establece el rango de tiempo.
        """
        self.time_range = time_range
        self.translator.set_time_range(time_range)
    
    def set_file_name(self, file_name):
        """
        Establece el nombre del archivo.
        """
        self.file_name = file_name
        self.translator.set_file_name(file_name)
    
    def set_translator_type(self, translator_type):
        """"
        Establece el tipo de traductor.
        """
        self.translator_type = translator_type
        self.set_translator()
    
    def set_method(self, method):
        """
        Establece el método numérico.
        """
        self.method = method
        self.check_components()
        self.translator.set_method(method)


    def add_equation(self, text_equation, text_var,constant):
        eq = Equation("a",text_equation, text_var, constant)
        self.equations.append(eq)

    def edit_equation(self, text_equation, text_var, constant, index):
        """
        Edita una ecuación existente en la lista de ecuaciones.
        """
        if index < 0 or index >= len(self.equations):
            raise IndexError("Índice fuera de rango.")
        
        eq = Equation("a",text_equation, text_var, constant)
        self.equations[index] = eq


    def check_components(self):
        """
        Verifica si los componentes son válidos.
        """
        # Verifica las ecuaciones
        for equation in self.equations:
            if not isinstance(equation, Equation):
                raise ValueError("Componente de ecuación inválido.")
            equation.check_components()

        # Verifica las condiciones
        for condition in self.conditions:
            if not isinstance(condition, Condition):
                raise ValueError("Componente de condición inválido.")
            condition.check_condition()

        # Verifica las condiciones iniciales. Comprobamos que cada variable de las ecuaciones
        # tenga un valor inicial.

        for equation in self.equations:
            for symbol in equation.get_simbol():
                if symbol not in self.initial_conditions:
                    raise ValueError(f"La variable {symbol} no tiene un valor inicial asignado.")
        
        # Verifica el rango de tiempo
        if not isinstance(self.time_range, list) or len(self.time_range) != 3:
            raise ValueError("El rango de tiempo debe ser una lista con tres elementos.")
        if not all(isinstance(i, (int, float)) for i in self.time_range):
            raise ValueError("El rango de tiempo debe contener solo números.")
        if self.time_range[0] >= self.time_range[1]:
            raise ValueError("El tiempo inicial debe ser menor que el tiempo final.")
        if self.time_range[2] <= 0:
            raise ValueError("El tamaño del paso debe ser mayor que cero.")
        
        # Verifica el nombre del archivo
        if not isinstance(self.file_name, str) or not self.file_name:
            raise ValueError("El nombre del archivo debe ser una cadena no vacía.")
        
    
        # Verifica el tipo de traductor
        if self.translator_type not in ["python", "cpp"]:
            raise ValueError("El tipo de traductor debe ser 'python' o 'cpp'.")
        
        # Verifica el método numérico
        if self.method not in ["euler", "rk4"]:
            raise ValueError("El método numérico debe ser 'euler' o 'rk4'.")
        
    

