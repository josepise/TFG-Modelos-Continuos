from app.equation import SimulationModel
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

