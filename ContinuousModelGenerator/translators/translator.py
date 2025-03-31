from abc import ABC, abstractmethod
from ..equation import Equation
import sympy as sp
import os

class SimulationModelGenerator(ABC):
    

    def __init__(self, equations, conditionals, initial_state, simulation_time, name_file, numerical_method="euler"):
        self.equations = equations
        self.conditionals = conditionals
        self.name_file = name_file
        self.numerical_method = numerical_method
        self.initial_state=initial_state
        self.simulation_time = simulation_time
    
    @abstractmethod
    def generate_file(self):
        pass


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

        #Definimos una lista de identificadores para las variables.
        self.var_identifiers = {}
        
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
    
        





    