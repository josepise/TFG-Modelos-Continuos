from .model import ContinuousModelGenerator as SimulationModel  #Importa la clase SimulationModel del archivo model.py
from view import SimulationView

class GeneratorController:
    
    def __init__ (self, root):
        self.model = SimulationModel()          #Creamos una instancia de la clase SimulationModel
        self.view = SimulationView(root, self)  #Crea la vista y le pasa el controlador
    

    def add_equation(self, equation):
        equation = self.view.get_equation_input()                               #Obtiene la ecuación ingresada por el usuario
        self.model.add_equation(equation)                                       #Agrega la ecuación al modelo
        self.view.clear_input()                                                 #Limpia el campo de entrada
        self.view.update_terminal(self.model.get_equations())                   #Actualiza la terminal con la ecuación ingresada

        self.view.update_equation_list(self.model.get_equations())             #Actualiza la lista de ecuaciones en la vista
        self.view.update_conditions_list(self.model.get_conditions())          #Actualiza la lista de condiciones en la vista
        self.view.update_initial_conditions_list(self.model.get_initial_conditions())
        self.view.update_time_range(self.model.get_time_range())               #Actualiza el rango de tiempo en la vista
        self.view.update_file_name(self.model.get_file_name())                 #Actualiza el nombre del archivo en la vista
        self.view.update_method(self.model.get_method())                       #Actualiza el método numérico en la vista
        self.view.update_translator_type(self.model.get_translator_type())     #Actualiza el tipo de traductor en la vista
        self.view.update_terminal(self.model.get_translator_type())            #Actualiza la terminal con el tipo de traductor
    
    