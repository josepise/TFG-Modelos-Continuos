from abc import ABC, abstractmethod
from ..equation import Equation
import sympy as sp
import os

class SimulationModelGenerator(ABC):
    

    def __init__(self, equations, conditionals, initial_conditions, simulation_time, path_file, name_file="simulation", numerical_method="euler"):
        self.equations = equations
        self.conditionals = conditionals
        self.path_file = path_file
        self.name_file = name_file
        self.numerical_method = numerical_method
        self.initial_conditions=initial_conditions
        self.simulation_time = simulation_time
        self.var_identifiers = {} # Diccionario para almacenar los identificadores de las variables.
        self.define_initial_sim()
    
    @abstractmethod
    def generate_file(self):
        pass


    def get_constants(self):
        """
        Get the constants of the equations and conditions.
        """
        return self.constants
    
    def get_var_identifiers(self):
        """
        Get the variable identifiers.
        """
        return self.var_identifiers
    
    def set_equations(self, equations):
        """
        Set the equations.
        """
        self.equations = equations
        self.set_var_identifiers()
        
    def set_conditions(self, conditions):
        """
        Set the conditions.
        """
        self.conditions = conditions
    
    def set_initial_conditions(self, initial_conditions):
        """
        Set the initial conditions.
        """
        self.initial_conditions = initial_conditions
    
    def set_time_range(self, time_range):
        """
        Set the time range.
        """
        self.simulation_time = time_range
    
    def set_file_name(self, file_name):
        """
        Set the file name.
        """
        self.file_name = file_name
    
    def set_method(self, method):
        """
        Set the numerical method.
        """
        self.numerical_method = method
    
    def set_directory(self, directory):
        """
        Set the directory for the generated file.
        """
        self.directory = directory

    def get_available_output(self, language):
        """
        Get the available output formats for a given language.
        """
        return self.available_output[language]

    def check_initial_state(self):

        #Comprobamos que cada variable de las ecuaciones tenga un valor inicial.
        try:
            for equation in self.equations:
                for symbol in equation.get_simbol():
                    if symbol not in self.initial_state:
                        raise ValueError(f"La variable {symbol} no tiene un valor inicial asignado.")
        except:
            symbol = equation.get_simbol()
            if symbol not in self.initial_state:
                raise ValueError(f"La variable {symbol} no tiene un valor inicial asignado.")

    def set_var_identifiers(self):
        """
        Establece los identificadores de las variables en las ecuaciones y condiciones.
        """
        index_var = 0 # Contador para los indices de las variables.

        #Iteramos sobre las ecuaciones y sus variables para definir un único identificador
        # por cada una. Las variables que tengan el mismo nombre se consideran la misma.
        for equation in self.equations:

            try:
                for symbol in equation.get_symbol():
                    if str(symbol) not in self.var_identifiers:
                        # Añadimos el símbolo a la lista de identificadores como string.
                        self.var_identifiers[str(symbol)] = index_var
                        index_var += 1
            except:
                symbol = str(equation.get_symbol())
                if symbol not in self.var_identifiers:
                    # Añadimos el símbolo a la lista de identificadores.
                    self.var_identifiers[symbol] = index_var
                    index_var += 1
    
    def set_constants(self) -> None:
        """
        Establece las constantes de las ecuaciones y condiciones.
        """
    
        self.constants = []
        self.constants_values = {}

        list_eq_cond=self.equations + self.conditionals
    
        # Iteramos sobre las ecuaciones y condiciones para obtener las constantes.
        for eq_cond in list_eq_cond:
            # Obtenemos los símbolos de la ecuación o condición.
            self.constants += eq_cond.get_constants()
            self.constants_values.update(eq_cond.get_constants_values())
    
        self.constants = list(set(self.constants))  # Eliminamos duplicados.

    def get_str_symbols(self) -> str:
        """
        Devuelve una cadena con los símbolos de las ecuaciones y condiciones.
        """
        symbols = ", ".join(self.constants) + ", ".join(self.var_identifiers.keys())

        str_constant=" ".join(f"<{x}>" for x in self.constants)
        str_var=" ".join(f"<{x}>" for x in self.var_identifiers.keys())
        
        return f"{str_constant} {str_var}"
    
    def get_constants(self) -> list:
        """
        Devuelve una lista con las constantes de las ecuaciones y condiciones.
        """
        return self.constants
    
    def get_constants_values(self) -> dict:
        """
        Devuelve un diccionario con los valores de las constantes de las ecuaciones y condiciones.
        """
        return self.constants_values
    
    def get_var_identifiers(self) -> dict:
        """
        Devuelve un diccionario con los identificadores de las variables.
        """
        return self.var_identifiers
    
    def get_initial_conditions(self) -> dict:
        """
        Devuelve un diccionario con las condiciones iniciales de las variables.
        """
        return self.initial_conditions

    def check_equations_conditions(self):
        """
        Comprueba que las condiciones contengan variables definidas en las ecuaciones.
        """

        # Creamos un conjunto de variables definidas en las ecuaciones.
        variables_equations = set()

        for equation in self.equations:
            variables_equations.update(equation.get_simbol())
        
        # Iteramos sobre las condiciones y comprobamos si contienen variables no definidas.
        for condition in self.conditionals:
            for symbol in condition.get_simbol():
                if symbol not in variables_equations:
                    raise ValueError(f"La variable {symbol} no está definida en las ecuaciones.")


    def define_initial_sim(self):
        """
        Define el estado inicial de la simulación.
        """

        if self.initial_conditions is None:
            self.initial_conditions = {}
            for equation in self.equations:
                for symbol in equation.get_symbol():
                    if str(symbol) not in self.initial_conditions:
                        self.initial_conditions[str(symbol)] = 0.0

        if self.simulation_time is None:
            self.simulation_time = [0,50,0.1] # [t0, tf, dt]





    