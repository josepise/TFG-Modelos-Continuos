from .model import ContinuousModelGenerator as SimulationModel  #Importa la clase SimulationModel del archivo model.py
from .view.main_view_ctk import GUI_CTK  as SimulationView  #Importa la clase SimulationView del archivo view.py
from .view.equation_view_ctk import GUI_Equation
from .view.condition_view_ctk import GUI_Condition


class GeneratorController:
    
    def __init__ (self):
        self.model = SimulationModel()        #Creamos una instancia de la clase SimulationModel
        self.view = SimulationView(self)  #Crea la vista y le pasa el controlador
        self.traductor=None                  #Inicializa el traductor como None
    

    def add_equation(self, text_equation:str, text_var:str, text_constant:str):
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
        var, text_equation, text_var, constants = self.prepare_equation(text_equation, text_var, text_constant)  

        #Añadimos la ecuación al modelo
        self.model.add_equation(var,text_equation, text_var, constants) 

        #Actualiza la lista de ecuaciones en la vista
        self.view.update_dropdown_equation(self.get_list_equations())           

    def add_condition(self, text_exp: str, text_act: str, text_var: str, text_constant: str):
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
                      
    def get_equation(self, name:str):
        
        #Quitamos Equation_ del name
        name = name.replace("Ecuacion_", "")
        name = int(name) - 1

        #Obtenemos la ecuación del modelo
        equation = self.model.get_equations()[name] 
    
        #Convertimos los elementos de la ecuación a texto
        equation_text = str(equation.get_equation())
        equation_name = equation.get_name()
        symbols_text = [str(sym) for sym in equation.get_symbol()]
        constants_text = [f"{key}={value}" for key, value in equation.get_constants_values().items()]
        
        #Adaptamos la salida para que sea más legible
        equation_text = equation_name + "=" + equation_text.replace(" ", "")
        symbols_text = " ".join(symbols_text).replace(" ", ",")
        constants_text = ",".join(constants_text)

        return equation_text, symbols_text, constants_text  
    
    def get_condition(self, name:str):
            
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

    def get_list_methods(self):
        return self.model.get_list_available_methods()            #Devuelve la lista de métodos disponibles
    
    def get_list_output(self):
        return self.model.get_list_available_output()           #Devuelve la lista de salidas disponibles
    
    def get_list_languages(self):
        return self.model.get_list_languages()                #Devuelve la lista de lenguajes disponibles
    
    def get_list_methods(self):
        return self.model.get_list_available_methods()                  #Devuelve la lista de métodos disponibles
    
    def get_variables(self):
        return list(self.model.get_variables())                             #Devuelve la lista de variables del modelo
    
    def get_parameters(self):
        return self.model.get_parameters()                            #Devuelve la lista de parámetros del modelo
    
    def edit_equation(self, text_equation:str, text_var:str, text_constant:str, name:str):
        name = name.replace("Ecuacion_", "")
        index = int(name) - 1

        name,text_equation, text_var, constants = self.prepare_equation(text_equation, text_var, text_constant)

        self.model.edit_equation(name,text_equation,text_var,constants, index)        

    def edit_condition(self, text_exp:str, text_act:str, text_var:str, text_constant:str, name:str):
        name = name.replace("Condicion_", "")
        index = int(name) - 1

        text_exp, text_act, text_var, constants = self.prepare_condition(text_exp, text_act, text_var, text_constant)

        self.model.edit_condition(text_exp,text_act,text_var,constants, index)

    def delete_equation(self, name:str):
        """
        Elimina una ecuación del modelo.
        Este método elimina una ecuación del modelo y actualiza la vista para reflejar
        los cambios en la lista de ecuaciones.
        Args:
            name (str): El nombre de la ecuación a eliminar. Debe estar en el formato "Ecuacion_i".
        Returns:
            None
        """        
        name = name.replace("Ecuacion_", "")
        index = int(name) - 1

        self.model.delete_equation(index)                                 
        self.view.update_dropdown_equation(self.get_list_equations())      

    def delete_condition(self, name:str):
        """
        Elimina una condición del modelo.
        Este método elimina una condición del modelo y actualiza la vista para reflejar
        los cambios en la lista de condiciones.
        Args:
            name (str): El nombre de la condición a eliminar. Debe estar en el formato "Condicion_i".
        Returns:
            None
        """        
        name = name.replace("Condicion_", "")
        index = int(name) - 1

        self.model.delete_condition(index)                                 
        self.view.update_dropdown_condition(self.get_list_conditions())      

    def set_language(self, language:str):
        self.model.set_translator_type(language)                  
        self.view.update_dropdown_output(self.get_list_output())      

    def set_method(self, method):
        self.model.set_method(method)                             

    def set_output(self, output):
        self.model.set_output_type(output)                         

    def prepare_equation(self, text_equation:str, text_var:str, text_constant:str):
         
        #Eliminamos los espacios en blanco de la ecuación
        text_equation = text_equation.replace(" ", "")  

        name, eq = text_equation.split("=")  #Dividimos la ecuación en nombre y ecuación


        #Eliminamos las comas en el texto de las variables
        text_var=text_var.replace(",", " ")

        #Eliminamos los espacios en blanco de las constantes
        text_constant = text_constant.replace(" ", "")

        #Convertirmos las constantes en un diccionario
        constants = {}

        if text_constant != "":
            for constant in text_constant.split(","):
                #Dividimos la constante en clave y valor
                if "=" in constant:
                    key, value = constant.split("=")
                elif constant != "":
                    key = constant
                    value = 0.0
                
                #Añadimos la constante al diccionario
                constants[key] = float(value)    

        return name, eq , text_var, constants

    def prepare_condition(self, text_exp:str, text_act:str, text_var:str, text_constant:str):
        
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
                elif constant != "":
                    key = constant
                    value = 0.0
                
                #Añadimos la constante al diccionario
                constants[key] = float(value)    

        return list_exp, list_act, text_var, constants

    def generate(self, path:str, name:str):
        """
        Genera el archivo de salida.
        Este método establece el lenguaje, el método numérico, el tipo de traductor, el rango 
        de tiempo y el nombre del archivo
        """

        self.model.set_file_name(name)                                          #Establece el nombre del archivo de salida
        self.model.set_path(path)                                               #Establece el directorio del archivo de salida
        self.model.set_translator()                                             #Establece el lenguaje
        self.model.generate_file()                                              #Genera el archivo de salida

        #Habilita el botón de simulación en la vista  
        self.view.simulate_button.configure(state="normal", fg_color="#3b8ed0", text_color="#FFFFFF")          

    def execute(self):
        """
        Ejecuta el archivo de salida.
        Este método ejecuta el archivo de salida generado por el modelo.
        """
        view_simulation=self.view.get_simulation_view()                        #Obtenemos la vista de simulación
        
        #Creamos la cadena de argumentos para la ejecución del archivo
        args=""
        entry_args=view_simulation.get_entries_args()                          #Obtenemos los argumentos de entrada de la vista

        for i in self.model.get_constants():
            args+= f"{entry_args[i].get()} "

        for i in self.model.get_var_identifiers():
            args+=f"{entry_args[i].get()} "


        time_args=view_simulation.get_time_args()                              #Obtenemos los argumentos de tiempo de la vista

        args+=f"{time_args['t0']} {time_args['tf']} {time_args['dt_tol']} "

        self.model.execute_simulation(args)                                           #Ejecuta el archivo de salida con los argumentos de entrada y tiempo

        translator_type = self.model.get_translator_type()                            #Obtenemos el tipo de traductor
        name_file=self.model.get_file_name()

        data = self.model.get_output_simulation_file(f"{name_file}_output_{translator_type}.csv")  # Obtenemos el archivo de salida
        
        view_simulation.update_result_terminal(data)
        view_simulation.update_result_plot(data)     

    def toggle_frame(self, mode:str=None ,option:str=None, selected:str=None):
        frame_width = self.view.aux_frame.winfo_width()  #Obtenemos el ancho del frame auxiliar
        
        if self.view.frame_open:
            self.view.hide_frame(frame_width)
            self.view.update_dropdown_condition(self.get_list_conditions())
            self.view.update_dropdown_equation(self.get_list_equations())
            self.view.update_dropdown_lang(self.get_list_languages())
            self.view.update_dropdown_output(self.get_list_output())
            self.view.update_dropdown_method(self.get_list_methods())
            
            if hasattr(self.view, 'eq_frm'):
                self.view.eq_frm.delete()
                del self.view.eq_frm

        else:
            aux_frame = GUI_Equation if mode == "eq" else GUI_Condition if mode == "cond" else None

            self.view.show_frame(frame_width ,aux_frame, option, selected)  
            self.view.dropdown_cond.pack_forget()
            self.view.dropdown_eq.pack_forget()
            self.view.dropdown_lang.pack_forget()
            self.view.dropdown_output.pack_forget()
            self.view.dropdown_method.pack_forget()
            self.view.add_condition_button.pack_forget()
            self.view.edit_condition_button.pack_forget()
            self.view.delete_condition_button.pack_forget()
            self.view.add_equation_button.pack_forget()
            self.view.edit_equation_button.pack_forget()
            self.view.delete_equation_button.pack_forget()
            
    def new_file(self):
        self.model=SimulationModel()                                         
        self.view.update_dropdown_condition(self.get_list_conditions())
        self.view.update_dropdown_equation(self.get_list_equations())
        self.view.update_dropdown_lang(self.get_list_languages())
        self.view.update_dropdown_output(self.get_list_output())
        self.view.update_dropdown_method(self.get_list_methods())


    def load_config(self, file_path:str):
        #Carga el archivo de configuración
        self.model=SimulationModel.load_config(file_path)                                         
        
        self.view.update_dropdown_condition(self.get_list_conditions())           
        self.view.update_dropdown_equation(self.get_list_equations())            
        self.view.update_dropdown_lang(self.get_list_languages(),self.model.get_translator_type())          
        self.view.update_dropdown_output(self.get_list_output(),self.model.get_output())            
        self.view.update_dropdown_method(self.get_list_methods(),self.model.get_method())           

    def save_config(self, file_path:str):
        self.model.save_config(file_path)                    


    
    def get_view(self):
        return self.view                                                        #Devuelve la vista del controlador