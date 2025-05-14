from customtkinter import CTkLabel
from datetime import datetime
from .log_codes import LOG_CODES

class LogHandler:
       
    def __init__(self):
        """Inicializa el manejador de errores."""
        self.log_codes = LOG_CODES
        self.log_label = None
        
    def set_log_label(self, label):
        """Establece la etiqueta de error de la interfaz gráfica."""
        self.log_label = label

    def generate_log_msg(self, code):
        """Genera un mensaje de consola a partir de un código de error."""
        message = self.log_codes.get(code, "Error desconocido.")

        # Añadimos al mensaje la hora del error
        current_time = datetime.now().strftime("%H:%M:%S")
        message = f"({current_time}) {message} "

        return message

    def generate_log_msg_prm(self, error_code, parameter):
        """Muestra un mensaje de consola con un parámetro adicional."""
        print(f"LogHandler: {error_code} - {parameter}")
        message = self.log_codes.get(error_code, "Error desconocido.")
        message = message.replace("{}", str(parameter))

        # Añadimos al mensaje la hora del error
        current_time = datetime.now().strftime("%H:%M:%S")
        message = f"({current_time}) {message} "
        
        return message
    
    def show_error(self, error_code):
        msg = self.generate_log_msg(error_code)
        self.log_label.configure(text=msg, text_color="red")
    
    def show_error_prm(self, error_code, parameter):
        msg = self.generate_log_msg_prm(error_code, parameter)
        self.log_label.configure(text=msg, text_color="red")

    def show_success(self, success_code):
        msg = self.generate_log_msg(success_code)
        self.log_label.configure(text=msg, text_color="green")
    
    def show_success_prm(self, success_code, parameter):
        msg = self.generate_log_msg_prm(success_code, parameter)
        self.log_label.configure(text=msg, text_color="green")

    def log_error(self, error_code):
        """Registra el error en consola o en un archivo de log."""
        message = self.errors.get(error_code, "Error desconocido.")
        print(f"Error - {error_code}: {message}")