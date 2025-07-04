import subprocess
from .translators import (python_translator, cpp_translator, java_translator, translator)
from .equation import Equation
from .conditions import Condition
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer, Image
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import importlib.util
import tempfile

import yaml, os


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
        self.output = None
        self.path_file = None
        self.available_output = {"java": ["csv"], "python": ["csv","plot"], "cpp": ["csv"]}
        self.available_methods = {"Euler": "euler", "Euler Mejorado": "euler-improved",
                                  "Runge Kutta 4": "runge-kutta-4", 
                                  "Runge Kutta Fehlberg": "runge-kutta-fehlberg"}
        self.packages = {"python":["python"], "cpp":["g++"], "java":["javac", "java"]}
        self.packages_linux = {"python":["python3"], "cpp":["g++"], "java":["javac", "java"]}
          
    def get_equations(self):
        """
        Obtiene las ecuaciones.
        """
        return self.equations
    
    def get_variables(self) :
        """
        Obtiene las variables de las ecuaciones.
        """
        return self.translator.get_var_identifiers().keys()
    
    def get_parameters(self):
        """
        Obtiene los parámetros de las ecuaciones.
        """
        return self.translator.get_constants()
    
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
        name=self.file_name
        if os.name != 'nt' and self.translator_type == "python":
            name=self.file_name[:-3]
        return name
    
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
    
    def get_output(self):
        """
        Obtiene el tipo de salida.
        """
        return self.output
    
    def get_list_languages(self):
        """
        Obtiene la lista de lenguajes disponibles.
        """
        return self.available_output.keys()
    
    def get_list_available_output(self):
        """
        Obtiene la lista de tipos de salida disponibles.
        """
        outputs= ["Seleccionar"]

        if self.translator_type is not None:
            outputs=self.available_output[self.translator_type]

        return outputs
    
    def get_constants(self):
        """
        Obtiene los parámetros de las ecuaciones y condiciones.
        """
        return self.translator.get_constants()
    
    def get_var_identifiers(self):

        """
        Obtiene los identificadores de las variables.
        """
        return self.translator.get_var_identifiers()
    
    def get_list_available_methods(self):
        """
        Obtiene la lista de métodos numéricos disponibles.
        """
        return self.available_methods.keys()
    
    def get_path(self):
        """
        Obtiene el directorio de salida.
        """
        return self.path_file

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
    
    def set_file_name(self, file_name):
        """
        Establece el nombre del archivo.
        """
        self.file_name = file_name

    def set_path(self, path):
        """
        Establece el directorio de salida.
        """
        self.path_file= path
    
    def set_translator_type(self, translator_type):
        """"
        Establece el tipo de traductor.
        """
        self.translator_type = translator_type
    
    def set_output(self, output):
        """
        Establece el tipo de salida.
        """
        self.output = output

    def set_method(self, method):
        """
        Establece el método numérico.
        """
        self.method = self.available_methods[method]

    def set_translator(self):
        if self.translator_type == "python":
            self.translator = python_translator.PythonSimulationGenerator(
                self.equations, self.conditions, self.initial_conditions, self.time_range, 
                self.path_file, self.file_name, self.output, self.method
            )
        elif self.translator_type == "cpp":
            self.translator = cpp_translator.CppSimulationGenerator(
                self.equations, self.conditions, self.initial_conditions, self.time_range, 
                self.path_file, self.file_name, self.method
            )
        elif self.translator_type == "java":
            self.translator = java_translator.JavaSimulationGenerator(
                self.equations, self.conditions, self.initial_conditions, self.time_range, 
                self.path_file, self.file_name, self.method
            )
        else:
            raise ValueError("Tipo de traductor inválido. Elija 'python', 'cpp' o 'java'.")
    
    def set_output_type(self, output_type):
        """
        Establece el tipo de salida.
        """
        self.output = output_type

    def add_equation(self,var_eq, text_equation, text_var,constant):
        eq = Equation(var_eq,text_equation, text_var, constant)
        error = eq.check_components()
        
        if error==(None, None):
            self.equations.append(eq)

        return error

    def edit_equation(self,var_eq, text_equation, text_var, constant, index):
        """
        Edita una ecuación existente en la lista de ecuaciones.
        """
        if index < 0 or index >= len(self.equations):
            raise IndexError("Índice fuera de rango.")
        
        eq = Equation(var_eq,text_equation, text_var, constant)
        error = eq.check_components()
        
        if error==(None, None):
            self.equations[index] = eq

        return error

    def delete_equation(self, index):
        """
        Elimina una ecuación de la lista de ecuaciones.
        """
        if index < 0 or index >= len(self.equations):
            raise IndexError("Índice fuera de rango.")
        
        del self.equations[index]

    def add_condition(self, text_exp ,  text_action, text_var,text_constant):
        cond = Condition(text_exp, text_action, text_var, text_constant)
        error = cond.check_components()
        
        if error==(None, None):
            self.conditions.append(cond)

        return error

    def edit_condition(self, text_exp ,  text_action, text_var,text_constant, index):
        """
        Edita una condición existente en la lista de condiciones.
        """
        if index < 0 or index >= len(self.conditions):
            raise IndexError("Índice fuera de rango.")
        
        cond = Condition(text_exp, text_action, text_var, text_constant)        
        error = cond.check_components()
        
        if error==(None, None):
            self.conditions[index] = cond
            
        return error
        
    def delete_condition(self, index):
        """
        Elimina una condición de la lista de condiciones.
        """
        if index < 0 or index >= len(self.conditions):
            raise IndexError("Índice fuera de rango.")
        
        del self.conditions[index]
        
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
        
    def execute_simulation(self,args):
        """
        Ejecuta la simulación utilizando el traductor seleccionado.
        """
        self.translator.run(args)

    def check_command(self, commands):
        # Ejecuta el comando y captura el código de salida
        missing_commands = ""
        # Si no es Windows
        
        if os.name != 'nt':  
            dict_commands = {
                "python3": "--version",
                "g++": "--version",
                "java": "-version",
                "javac": "-version"
            }
        else:  # Si es Windows
            dict_commands = {
                "python": "--version",
                "g++": "--version",
                "java": "-version",
                "javac": "-version"
            }
        
        for command in commands:
            exit_code = os.system(f"{command} {dict_commands[command]} >nul 2>&1")
            if exit_code != 0:
                missing_commands += f"{command} "

        # Comprobar si numpy está instalado
        if self.translator_type=="python":
            try:
                result = subprocess.run(
                    ["pip", "show", "numpy"],
                    capture_output=True, text=True, check=True
                )
                
                if "Name: numpy" in result.stdout:
                    pass
                else:
                    missing_commands += "numpy "
            except subprocess.CalledProcessError:
                result = subprocess.run(
                    ["pipx","list"],
                    capture_output=True, text=True, check=True
                )
                
                if "numpy" in result.stdout:
                    pass
                else:
                    missing_commands += "numpy "      


        return missing_commands
        

    def check_generation(self):

        # Comprobamos que haya sido establecido el lenguaje, la salida , 
        # el método y al menos una ecuación
        if self.get_translator_type() == None:
            return ("GENERATION_FAILED_NO_LANGUAGE", None)
        elif self.get_output() == None:
            return ("GENERATION_FAILED_NO_OUTPUT", None)
        elif len(self.get_equations()) == 0:
            return ("GENERATION_FAILED_NO_EQUATIONS", None)
        
        # Comprobar que los nombres de las ecuaciones están en get_var_identifiers
        equation_names = [str(eq.get_name()) for eq in self.get_equations()]
        symbols = list(set([str(symbol) for eq in self.get_equations() for symbol in eq.get_symbol()]))
       
        missing_names = [name for name in equation_names if name not in symbols]
        if missing_names:
            return ("GENERATION_FAILED_MISSING_VARS", missing_names)
        
        return (None, None)


    def check_compiler(self):
        #Comprobamos que se encuentra en Windows
        if os.name == 'nt':
            packages = self.packages
        else:  
            packages = self.packages_linux

        missing_commands = self.check_command(packages[self.get_translator_type()])
        
        if missing_commands:
            return ("GENERATION_FAILED_NO_COMPILER", missing_commands)
        
        return (None, None)
    
    def compile(self):
        """
        Compila el código generado por el traductor.
        """
        self.translator.compile()

    def get_output_simulation_file(self, file_path):
        """
        Lee el archivo de salida de la simulación y devuelve su contenido.
        """
        with open(file_path) as f:
            lines = f.readlines()
            content = [line.strip().split() for line in lines]
        
        return content
    
    def export_pdf(self, text, fig, params, time ,filename="resultado_exportado.pdf"):
        # Crear documento PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elementos = []

        style_table = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ])

        #Título
        estilos = getSampleStyleSheet()
        titulo = Paragraph("Resultados de la Simulación", estilos["Title"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))

        # Añadimos características de la simulación
        
        #Tipo de traductor
        tipo_traductor = Paragraph(f"<b>Tipo de Traductor:</b> {self.translator_type.capitalize()}", estilos["Normal"])
        elementos.append(tipo_traductor)
        elementos.append(Spacer(1, 12))

        #Método numérico
        metodo = Paragraph(f"<b>Método Numérico:</b> {self.method.capitalize()}", estilos["Normal"])
        elementos.append(metodo)
        elementos.append(Spacer(1, 12))

        #Intervalos de tiempo
        if self.method == "runge-kutta-fehlberg":
            tiempo = Paragraph(f"<b>Rango de Tiempo:</b> {time['t0']} a {time['tf']} con tolerancia de {time['dt_tol']}", estilos["Normal"])
        else:
            tiempo = Paragraph(f"<b>Rango de Tiempo:</b> {time['t0']} a {time['tf']} con paso de {time['dt_tol']}", estilos["Normal"])
        elementos.append(tiempo)
        elementos.append(Spacer(1, 12))
    
        #Valores de los parámetros y variables
        parametros = Paragraph("<b>Parámetros y Variables:</b>", estilos["Normal"])
        elementos.append(parametros)
        elementos.append(Spacer(1, 12))
        
        #Añadir tabla con Nombre del parámetro y valor
        rows = []
        rows.append(["Nombre", "Valor"])
        for param, value in params.items():
            rows.append([param, value])
        tabla_parametros = Table(rows, colWidths=[2*inch, 3*inch])
        tabla_parametros.setStyle(style_table)
        elementos.append(tabla_parametros)
        elementos.append(Spacer(1, 12))

        # Añadir tabla de ecuaciones
        ecuaciones = Paragraph("<b>Ecuaciones:</b>", estilos["Normal"])
        elementos.append(ecuaciones)
        elementos.append(Spacer(1, 12))
        rows = []
        rows.append(["Ecuación"])
        for eq in self.get_equations():
            text_eq = f"d{eq.get_name()}/dt={eq.get_text_equation()}"
            rows.append([text_eq])
            
        tabla_ecuaciones = Table(rows, colWidths=[5*inch])
        tabla_ecuaciones.setStyle(style_table)
        elementos.append(tabla_ecuaciones)
        elementos.append(Spacer(1, 12))

        # Añadir tabla de condiciones
        if len(self.get_conditions()) > 0:
            condiciones = Paragraph("<b>Condiciones:</b>", estilos["Normal"])
            elementos.append(condiciones)
            elementos.append(Spacer(1, 12))
            rows = []
            rows.append(["Condición", "Acción"])
            for cond in self.get_conditions():
                rows.append([cond.get_text_condition(), cond.get_text_result()])
            tabla_condiciones = Table(rows, colWidths=[3*inch, 2*inch])
            tabla_condiciones.setStyle(style_table)
            elementos.append(tabla_condiciones)
            elementos.append(Spacer(1, 12))
            
        #Guardar imagen del gráfico temporalmente
        temp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig.savefig(temp_img.name, dpi=300, bbox_inches="tight")

        #Insertar gráfico
        imagen = Image(temp_img.name, width=5*inch, height=3*inch)
        elementos.append(imagen)
        elementos.append(Spacer(1, 20))

        # Reemplazar ' ' por tabulaciones
        text = text.replace(' ', '\t')

        # Eliminamos la segunda linea que contiene guiones y añadimos 
        lines = text.strip().split('\n')      
        text = '\n'.join([lines[0]] + lines[2:])

        rows = [line.strip().split('\t') for line in text.strip().split('\n') if line.strip()]
        

        # Tabla formateada
        tabla = Table(rows,colWidths=[1.5*inch]*len(rows[0]))
        tabla.setStyle(style_table)

        elementos.append(tabla)

        # 4. Guardar el PDF
        doc.build(elementos)

        print(f"PDF exportado correctamente como {filename}")


    def save_config(self, file_path):
        """
        Guarda la configuración actual en un archivo.
        """
        config = {
            "equation":[ 
                {
                    "name": eq.get_name(),
                    "expression": eq.get_text_equation(),
                    "variable": eq.get_text_symbol(),
                    "parameters": eq.get_constants_values()
                } for eq in self.equations
            ],
            "conditions": [
                {
                    "expressions": cond.get_text_condition(),
                    "actions": cond.get_text_result(),
                    "variables": cond.get_text_symbols(),
                    "parameters": cond.get_constants_values()
                } for cond in self.conditions
            ],
            "simulation": {
                "time": self.time_range,
                "output_file": self.file_name,
                "output_format": self.output,   
                "translator": self.translator_type,
                "method": self.method
            }
        }

        with open(file_path, "w") as file:
            yaml.dump(config, file, sort_keys=False)

    @classmethod
    def load_config(cls, file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)

        equation = [
            Equation(eq["name"], eq["expression"], eq["variable"], eq["parameters"])
            for eq in config["equation"]
        ]

        conditions = [
            Condition(
            c["expressions"].split(",") if "," in c["expressions"] else [c["expressions"]],
            c["actions"].split(",") if "," in c["actions"] else [c["actions"]],
            c["variables"],
            c["parameters"]
            )
            for c in config["conditions"]
        ]

        sim_data = config["simulation"]

        instance = cls()
        instance.equations = equation
        instance.conditions = conditions
        instance.time_range = sim_data["time"]
        instance.file_name = sim_data["output_file"]
        instance.method = sim_data["method"]
        instance.translator_type = sim_data["translator"]
        instance.output = sim_data["output_format"]
        return instance
