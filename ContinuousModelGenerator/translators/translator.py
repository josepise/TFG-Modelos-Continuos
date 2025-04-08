from abc import ABC, abstractmethod
from ..equation import Equation
import sympy as sp
import os

class SimulationModelGenerator(ABC):
    

    def __init__(self, equations, conditionals, initial_conditions, simulation_time, name_file, numerical_method="euler"):
        self.equations = equations
        self.conditionals = conditionals
        self.name_file = name_file
        self.numerical_method = numerical_method
        self.initial_conditions=initial_conditions
        self.simulation_time = simulation_time
        self.var_identifiers = {} # Diccionario para almacenar los identificadores de las variables.
    
    @abstractmethod
    def generate_file(self):
        pass

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

        #Comprobamos que cada variable de las ecuaciones tenga un valor inicial.
        # self.check_initial_state()

        index_var = 0 # Contador para los indices de las variables.

        #Iteramos sobre las ecuaciones y sus variables para definir un único identificador
        # por cada una. Las variables que tengan el mismo nombre se consideran la misma.
        for equation in self.equations:

            try:
                for symbol in equation.get_simbol():
                    if str(symbol) not in self.var_identifiers:
                        # Añadimos el símbolo a la lista de identificadores como string.
                        self.var_identifiers[str(symbol)] = index_var
                        index_var += 1
            except:
                symbol = str(equation.get_simbol())
                if symbol not in self.var_identifiers:
                    # Añadimos el símbolo a la lista de identificadores.
                    self.var_identifiers[symbol] = index_var
                    index_var += 1
    
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





    