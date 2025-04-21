from .model import ContinuousModelGenerator as SimulationModel  #Importa la clase SimulationModel del archivo model.py
from .equation import Equation  #Importa la clase Equation del archivo equation.py
from .view.main_view import GUI as SimulationView  #Importa la clase SimulationView del archivo view.py
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
        text_equation, text_var, constants = self.prepare_equation(text_equation, text_var, text_constant)  

        #Añadimos la ecuación al modelo
        self.model.add_equation(text_equation, text_var, constants) 

        #Actualiza la lista de ecuaciones en la vista
        self.view.update_dropdown_equation(self.get_list_equations())           

    def add_condition(self,text_exp, text_act, text_var, text_constant):
        """
        Añade una condición al modelo.
        Este método procesa una condición proporcionada por el usuario, junto con las variables
        y constantes asociadas, y la añade al modelo. Además, actualiza la vista para reflejar
        los cambios en la lista de condiciones.
        Args:
            text_exp (str): La expresión de la condición en formato de texto. Los espacios en blanco serán eliminados.
            text_act (str): La acción a realizar si se cumple la condición. Los espacios en blanco serán eliminados.
            text_var (str): Las variables de la condición, separadas por comas. Las comas serán reemplazadas por espacios.
            text_constant (str): Las constantes de la condición en formato "clave=valor", separadas por comas. Si no se 
                                 proporciona un valor, se asignará 0.0 por defecto.
        Returns:
            None
        """        
        list_exp, list_act, text_var, constants = self.prepare_condition(text_exp, text_act, text_var, text_constant)  

        #Añadimos la condición al modelo
        self.model.add_condition(list_exp,list_act, text_var, constants) 

        #Actualiza la lista de condiciones en la vista
        self.view.update_dropdown_condition(self.get_list_conditions())
                      
    def get_equation(self, name):
        
        #Quitamos Equation_ del name
        name = name.replace("Ecuacion_", "")
        name = int(name) - 1

        #Obtenemos la ecuación del modelo
        equation = self.model.get_equations()[name] 
    
        #Convertimos los elementos de la ecuación a texto
        equation_text = str(equation.get_equation())
        symbols_text = [str(sym) for sym in equation.get_symbol()]
        constants_text = [f"{key}={value}" for key, value in equation.get_constants_values().items()]
        
        #Adaptamos la salida para que sea más legible
        equation_text = equation_text.replace(" ", "")
        symbols_text = " ".join(symbols_text).replace(" ", ",")
        constants_text = ",".join(constants_text)

        return equation_text, symbols_text, constants_text  
    
    def get_condition(self, name):
            
            #Quitamos Condicion_ del name
            name = name.replace("Condicion_", "")
            name = int(name) - 1
    
            #Obtenemos la condición del modelo
            condition = self.model.get_conditions()[name] 
        
            #Obtenemos los elementos de la condición
            condition_text = condition.get_text_condition()
            action_text = condition.get_text_result()
            symbols_text = condition.get_text_symbols()
            constants_text = condition.get_text_constants()
                    
            return condition_text, action_text, symbols_text, constants_text
       
    def get_list_equations(self):
        #Formamos una lista compuesta por Ecuacion_i, donde i es el número de la ecuación
        equations = self.model.get_equations()                                          
        
        if len(equations) > 0:                                    #Si hay ecuaciones
            list_equations = []
        
            for i in range(len(equations)):
                list_equations.append(f"Ecuacion_{i+1}")          #Añadimos la ecuación a la lista
        else:
            list_equations = None
       
        return list_equations                                   
    
    def get_list_conditions(self):
        #Formamos una lista compuesta por Condición_i, donde i es el número de la condición
        conditions = self.model.get_conditions()                                          
        
        if len(conditions) > 0:                                    #Si hay condiciones
            list_conditions = []
        
            for i in range(len(conditions)):
                list_conditions.append(f"Condicion_{i+1}")          #Añadimos la condición a la lista
        else:
            list_conditions = None
       
        return list_conditions                                    

    def edit_equation(self, text_equation, text_var, text_constant, name):
        name = name.replace("Ecuacion_", "")
        index = int(name) - 1

        text_equation, text_var, constants = self.prepare_equation(text_equation, text_var, text_constant)

        self.model.edit_equation(text_equation,text_var,constants, index)        

    def edit_condition(self, text_exp, text_act, text_var, text_constant, name):
        name = name.replace("Condicion_", "")
        index = int(name) - 1

        text_exp, text_act, text_var, constants = self.prepare_condition(text_exp, text_act, text_var, text_constant)

        self.model.edit_condition(text_exp,text_act,text_var,constants, index)

    def prepare_equation(self, text_equation, text_var, text_constant):
         
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

        return text_equation, text_var, constants

    def prepare_condition(self, text_exp, text_act, text_var, text_constant):
        
        #Eliminamos los espacios en blanco de la ecuación
        text_exp = text_exp.replace(" ", "")  

        # Formamos una lista donde cada elemento se encuentra separado con una coma en el string
        if "," in text_exp:
            list_exp = text_exp.split(",")
        else:
            list_exp = [text_exp]  
        
        if "," in text_act:
            list_act = text_act.split(",")
        else:
            list_act = [text_act]

        #Eliminamos las comas en el texto de las variables
        text_var=text_var.replace(",", " ")

        #Convertirmos las constantes en un diccionario
        constants = {}
        if text_constant != "":
            for constant in text_constant.split(","):
                #Dividimos la constante en clave y valor
                if "=" in constant:
                    key, value = constant.split("=")
                else:
                    key = constant
                    value = 0.0
                
                #Añadimos la constante al diccionario
                constants[key] = float(value)    

        return list_exp, list_act, text_var, constants

    def generate(self):
        self.model.generate_file()                                              #Genera el archivo de salida


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