from .model import ContinuousModelGenerator as SimulationModel  #Importa la clase SimulationModel del archivo model.py
from .view import GUI as SimulationView  #Importa la clase SimulationView del archivo view.py
from sympy import symbols, sympify


class GeneratorController:
    
    def __init__ (self):
        self.model = SimulationModel()        #Creamos una instancia de la clase SimulationModel
        self.view = SimulationView(self)  #Crea la vista y le pasa el controlador
        self.traductor=None                  #Inicializa el traductor como None
    

    def add_equation(self, text_equation, text_var, text_constant):
        """
        Añade una ecuación al modelo.
        Este método procesa una ecuación proporcionada por el usuario, junto con las variables
        y constantes asociadas, y la añade al modelo. Además, actualiza la vista para reflejar
        los cambios en la lista de ecuaciones.
        Args:
            text_equation (str): La ecuación en formato de texto. Los espacios en blanco serán eliminados.
            text_var (str): Las variables de la ecuación, separadas por comas. Las comas serán reemplazadas por espacios.
            text_constant (str): Las constantes de la ecuación en formato "clave=valor", separadas por comas. Si no se 
                                 proporciona un valor, se asignará 0.0 por defecto.
        Returns:
            None
        """        
        
        #Eliminamos los espacios en blanco de la ecuación
        text_equation = text_equation.replace(" ", "")  
        

        #Eliminamos las comas en el texto de las variables
        text_var=text_var.replace(",", " ")

        #Convertirmos las constantes en un diccionario
        constants = {}
        for constant in text_constant.split(","):
            #Dividimos la constante en clave y valor
            if "=" in constant:
                key, value = constant.split("=")
            else:
                key = constant
                value = 0.0
            
            #Añadimos la constante al diccionario
            constants[key] = float(value)

        #Añadimos la ecuación al modelo
        self.model.add_equation(text_equation, text_var, constants) 

        #Actualiza la lista de ecuaciones en la vista
        self.view.update_dropdown_equation(self.get_list_equations())           

       
    def get_list_equations(self):
        #Formamos una lista compuesta por Ecuacion_i, donde i es el número de la ecuación
        equations = self.model.get_equations()                                          
        
        if len(equations) > 0:                                                        #Si no hay ecuaciones
            list_equations = []
        
            for i, equation in enumerate(equations):
                list_equations.append(f"Ecuacion_{i+1}")                                   #Añadimos la ecuación a la lista
        else:
            list_equations = None
       
        return list_equations                                                          #Devolvemos la lista de ecuaciones
    

    def delete_equation(self, equation):
        self.model.delete_equation(equation)                                   #Elimina la ecuación del modelo
        self.view.update_terminal(self.model.get_equations())                  #Actualiza la terminal con la ecuación eliminada
        self.view.update_equation_list(self.model.get_equations())             #Actualiza la lista de ecuaciones en la vista
        self.view.update_conditions_list(self.model.get_conditions())          #Actualiza la lista de condiciones en la vista
        self.view.update_initial_conditions_list(self.model.get_initial_conditions())
        self.view.update_time_range(self.model.get_time_range())               #Actualiza el rango de tiempo en la vista
        self.view.update_file_name(self.model.get_file_name())                 #Actualiza el nombre del archivo en la vista
        self.view.update_method(self.model.get_method())                       #Actualiza el método numérico en la vista
        self.view.update_translator_type(self.model.get_translator_type())     #Actualiza el tipo de traductor en la vista
    
    def edit_equation(self, equation):
        self.model.edit_equation(equation)                                     #Edita la ecuación en el modelo
        self.view.update_terminal(self.model.get_equations())                  #Actualiza la terminal con la ecuación editada
        self.view.update_equation_list(self.model.get_equations())             #Actualiza la lista de ecuaciones en la vista
        self.view.update_conditions_list(self.model.get_conditions())          #Actualiza la lista de condiciones en la vista
        self.view.update_initial_conditions_list(self.model.get_initial_conditions())
        self.view.update_time_range(self.model.get_time_range())               #Actualiza el rango de tiempo en la vista
        self.view.update_file_name(self.model.get_file_name())                 #Actualiza el nombre del archivo en la vista
        self.view.update_method(self.model.get_method())                       #Actualiza el método numérico en la vista
        self.view.update_translator_type(self.model.get_translator_type())     #Actualiza el tipo de traductor en la vista
    
    def clear_fields(self):
        self.view.clear_input()                                                 #Limpia el campo de entrada
        self.view.update_terminal(self.model.get_equations())                   #Actualiza la terminal con la ecuación eliminada
        self.view.update_equation_list(self.model.get_equations())             #Actualiza la lista de ecuaciones en la vista
        self.view.update_conditions_list(self.model.get_conditions())          #Actualiza la lista de condiciones en la vista
        self.view.update_initial_conditions_list(self.model.get_initial_conditions())
        self.view.update_time_range(self.model.get_time_range())               #Actualiza el rango de tiempo en la vista
        self.view.update_file_name(self.model.get_file_name())                 #Actualiza el nombre del archivo en la vista
        self.view.update_method(self.model.get_method())                       #Actualiza el método numérico en la vista
        self.view.update_translator_type(self.model.get_translator_type())     #Actualiza el tipo de traductor en la vista
    
    def generate_simulation(self):
        self.model.generate_file()                                              #Genera el archivo de salida
        self.view.update_terminal(self.model.get_equations())                   #Actualiza la terminal con la ecuación generada
        self.view.update_equation_list(self.model.get_equations())             #Actualiza la lista de ecuaciones en la vista
        self.view.update_conditions_list(self.model.get_conditions())          #Actualiza la lista de condiciones en la vista
        self.view.update_initial_conditions_list(self.model.get_initial_conditions())
        self.view.update_time_range(self.model.get_time_range())               #Actualiza el rango de tiempo en la vista
        self.view.update_file_name(self.model.get_file_name())                 #Actualiza el nombre del archivo en la vista
        self.view.update_method(self.model.get_method())                       #Actualiza el método numérico en la vista
        self.view.update_translator_type(self.model.get_translator_type())     #Actualiza el tipo de traductor en la vista
    
    def get_view(self):
        return self.view                                                        #Devuelve la vista del controlador