from tkinter import Button, Tk, Canvas, Menu , filedialog
from tkinter import StringVar, OptionMenu, PhotoImage
from .equation_view import GUI_Equation
from .condition_view import GUI_Condition
import os

class GUI:
    def __init__(self, controller=None):
        #Definimos la ruta de la carpeta de recursos de imágenes
        self.route_img = os.path.join("ContinuousModelGenerator","resources", "img")
        
        #Añadimos el controlador a la vista
        self.controller = controller

        self.window = Tk()
        self.window.geometry("811x468")
        self.window.configure(bg="#92A6C0")
        self.window.resizable(False, False)

        self.canvas = Canvas(
            self.window,
            bg="#92A6C0",
            height=468,
            width=811,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.load_imgs()
        self.create_widgets()


    def load_imgs(self):
        self.add_img = PhotoImage(file=os.path.join(self.route_img, 'add.png'))
        self.edit_img = PhotoImage(file=os.path.join(self.route_img, 'edit.png'))

    def create_widgets(self):
        
        self.top_menu()

        # Cuadro de texto elegir lenguaje
        self.canvas.create_text(
            27.0,
            26.0,
            anchor="nw",
            text="Lenguaje",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )
        
        # Lista desplegable de lenguajes
        self.update_dropdown_lang(self.controller.get_list_languages())

        # Lista desplegable de tipos de salida
        self.canvas.create_text(
            27.0,
            58.0,
            anchor="nw",
            text="Salida",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )

        self.update_dropdown_output(self.controller.get_list_output())

        # Lista desplegable de tipos de salida
        self.canvas.create_text(
            27.0,
            97.0,
            anchor="nw",
            text="Método \nIntegración",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )

        self.update_dropdown_method(self.controller.get_list_methods())

        self.widget_equation()
        
        self.widget_condition()
        
        self.generate_button = Button(
            self.window,
            text="Generar",
            command=self.generate_program,
            bg="#D9D9D9"
        )
        self.generate_button.place(x=659.0, y=399.0, width=125.0, height=50.0)


    def top_menu(self):
        menu_bar = Menu(self.window)

        menu_archivo = Menu(menu_bar, tearoff=0)
        menu_archivo.add_command(label="Nuevo")#, command=nuevo_archivo)
        menu_archivo.add_command(label="Abrir", command=self.open_config_file)
        menu_archivo.add_command(label="Guardar", command=self.save_config_file)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir")#, command=salir)
        menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú "Ver"
        menu_ver = Menu(menu_bar, tearoff=0)
        menu_ver.add_checkbutton(label="Mostrar líneas de tiempo")
        menu_bar.add_cascade(label="Ver", menu=menu_ver)

        # Menú "Ayuda"
        menu_ayuda = Menu(menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Ver Ayuda")#, command=mostrar_ayuda)
        menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Asociar la barra de menú con la ventana
        self.window.config(menu=menu_bar)

    def widget_equation(self):

        #Cuadro de texto de Ecuaciones
        self.canvas.create_text(
            16.0,
            139.0,
            anchor="nw",
            text="Ecuaciones",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )

        #Lista desplegable de ecuaciones
        self.update_dropdown_equation(self.controller.get_list_equations())

        self.add_equation_button = Button(
            self.window,
            text="Añadir",
            image=self.add_img,
            command=lambda: GUI_Equation(self.window, self.controller, "add"),
            borderwidth=0,
            background="#92A6C0",
            highlightthickness=0,
            relief="flat"
        )
        self.add_equation_button.place(x=317.0, y=136.0, width=20.0, height=20.0)

        self.edit_equation_button = Button(
            self.window,
            text="Editar",
            image=self.edit_img,
            command=self.modify_equation,
            borderwidth=0,
            background="#92A6C0",
            highlightthickness=0,
            relief="flat"
        )
        self.edit_equation_button.place(x=349.0, y=136.0, width=20.0, height=20.0)

    def widget_condition(self):

        self.canvas.create_text(
            10.0,
            179.0,
            anchor="nw",
            text="Condiciones",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )

        self.update_dropdown_condition(self.controller.get_list_conditions())

        self.add_condition_button = Button(
            self.window,
            text="Añadir",
            image=self.add_img,
            command=lambda: GUI_Condition(self.window, self.controller, "add"),
            borderwidth=0,
            background="#92A6C0",
            highlightthickness=0,
            relief="flat"
        )

        self.add_condition_button.place(x=317.0, y=176.0, width=20.0, height=20.0)

        self.edit_condition_button = Button(
            self.window,
            text="Editar",
            image=self.edit_img,
            command=self.modify_condition,
            borderwidth=0,
            background="#92A6C0",
            highlightthickness=0,
            relief="flat"
        )

        self.edit_condition_button.place(x=349.0, y=176.0, width=20.0, height=20.0)

    def update_dropdown_condition(self,options):
        self.dropdown_cond = StringVar(self.window)
        self.dropdown_cond.set("Seleccionar")  #Valor por defecto
        
        if not options:  #Nos aseguramos que existan opciones
            options = ["No existen condiciones."]

        self.dropdown_menu_cond = OptionMenu(
            self.window,
            self.dropdown_cond,
            *options
        )
        self.dropdown_menu_cond.place(x=104.0, y=176.0, width=198.0, height=20.0)
        
    def update_dropdown_equation(self, options):
        self.dropdown_eq = StringVar(self.window)
        self.dropdown_eq.set("Seleccionar")  #Valor por defecto
        
        if not options:  #Nos aseguramos que existan opciones
            options = ["No existen ecuaciones."]

        self.dropdown_menu_eq= OptionMenu(
            self.window,
            self.dropdown_eq,
            *options
        )
        self.dropdown_menu_eq.place(x=104.0, y=136.0, width=198.0, height=20.0)

    def update_dropdown_lang(self, options, selected_option=None):
        self.dropdown_lang = StringVar(self.window)
        self.dropdown_lang.set("Seleccionar")
        
        if selected_option:
            self.dropdown_lang.set(selected_option)
        
        self.dropdown_menu_lang = OptionMenu(
            self.window,
            self.dropdown_lang,
            *options,
            command=self.controller.set_language
        )
        self.dropdown_menu_lang.place(x=104.0, y=26.0, width=198.0, height=20.0)

    def update_dropdown_output(self, options, selected_option=None):
        self.dropdown_output = StringVar(self.window)
        self.dropdown_output.set("Seleccionar")

        if selected_option:
            self.dropdown_output.set(selected_option)

        self.dropdown_menu_output = OptionMenu(
            self.window,
            self.dropdown_output,
            *options,
            command=self.controller.set_output
        )
        self.dropdown_menu_output.place(x=104.0, y=58.0, width=198.0, height=20.0)

    def update_dropdown_method(self, options, selected_option=None):
        self.dropdown_method = StringVar(self.window)
        self.dropdown_method.set("Seleccionar")

        if selected_option:
            self.dropdown_method.set(selected_option)

        self.dropdown_menu_method = OptionMenu(
            self.window,
            self.dropdown_method,
            *options,
            command=self.controller.set_method
        )
        self.dropdown_menu_method.place(x=104.0, y=97.0, width=198.0, height=20.0)
    
    def modify_equation(self):
        selected_equation = self.dropdown_eq.get()
        if selected_equation != "Seleccionar":
            GUI_Equation(self.window, self.controller, "edit", selected_equation)
        else:
            print("No equation selected")   

    def modify_condition(self):
        selected_condition = self.dropdown_cond.get()
        if selected_condition != "Seleccionar":
            GUI_Condition(self.window, self.controller, "edit", selected_condition)
        else:
            print("No condition selected")


    def open_config_file(self):
        ruta = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")], title="Selecciona un archivo")
        if ruta:
            self.controller.load_config(ruta)

    def save_config_file(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".yaml", title="Guardar archivo")
        if ruta:
            self.controller.save_config(ruta)
        
    def generate_program(self):
        ruta_completa = filedialog.asksaveasfilename(title="Generar programa")
        
        if ruta_completa:
            ruta, nombre = os.path.split(ruta_completa)
            self.controller.generate(ruta, nombre)

    def run(self):
        self.window.mainloop()


