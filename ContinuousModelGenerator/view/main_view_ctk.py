import customtkinter as ctk
from customtkinter import CTkImage 
from tkinter import Menu, filedialog
from PIL import Image
import os
from .equation_view import GUI_Equation
from .condition_view import GUI_Condition
from .simulation_view import GUI_Simulation

class GUI_CTK:
    def __init__(self, controller=None):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.route_img = os.path.join("ContinuousModelGenerator", "resources", "img")
        self.controller = controller

        # Colores de la interfaz
        self.color_bg = "#352F6B"
        self.color_text = "#ECEDF1"
        self.color_button_drop = "#058CB1"
        self.color_dropdown = "#ECEDF1"
        self.color_aux = "#352F6B"

        self.window = ctk.CTk()
        self.window.geometry("811x468")
        self.window.configure(fg_color=self.color_bg)
        self.window.resizable(False, False)
        # self.window.overrideredirect(True)

        self.load_imgs()
        self.create_widgets()

    def init_sim_view(self):
        self.simulation_view = GUI_Simulation(self.window, self.controller)


    def get_simulation_view(self):
        return self.simulation_view
    
    def load_imgs(self):
        self.add_img = CTkImage(light_image=Image.open(os.path.join(self.route_img, 'add.png')), size=(20, 20))
        self.edit_img = CTkImage(light_image=Image.open(os.path.join(self.route_img, 'edit.png')), size=(20, 20))

    def create_widgets(self):
        self.top_menu()

        self.create_label("Lenguaje", 23, 26)
        options = list(self.controller.get_list_languages())
        self.update_dropdown_lang(options)

        self.create_label("Salida", 23, 58)
        options = list(self.controller.get_list_output())
        self.update_dropdown_output(options)

        self.create_label("Método\nIntegración", 23, 97)
        options = list(self.controller.get_list_methods())
        self.update_dropdown_method(options)

        self.widget_equation()
        self.widget_condition()

        self.generate_button = ctk.CTkButton(
            self.window, text="Generar", command=self.generate_program, width=125, height=50
        )
        self.generate_button.place(x=659, y=399)

        self.simulate_button = ctk.CTkButton(
            self.window, text="Simular", command=self.init_sim_view, width=125, height=50
        )
        self.simulate_button.place(x=520, y=399)

    def create_label(self, text, x, y):
        label = ctk.CTkLabel(self.window, text=text, text_color=self.color_text, font=("Roboto", 12, "bold"), anchor="w", justify="left")
        label.place(x=x, y=y)

    def top_menu(self):
        menu_bar = Menu(self.window, relief="flat")

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
        self.create_label("Ecuaciones", 23, 139)
        self.update_dropdown_equation(self.controller.get_list_equations())

        self.add_equation_button = ctk.CTkButton(
            self.window, text="", image=self.add_img, command=lambda: GUI_Equation(self.window, self.controller, "add"), width=20, height=20, fg_color="transparent"
        )
        self.add_equation_button.place(x=317, y=136)

        self.edit_equation_button = ctk.CTkButton(
            self.window, text="", image=self.edit_img, command=self.modify_equation, width=20, height=20, fg_color="transparent"
        )
        self.edit_equation_button.place(x=349, y=136)

    def widget_condition(self):
        self.create_label("Condiciones", 23, 179)
        self.update_dropdown_condition(self.controller.get_list_conditions())

        self.add_condition_button = ctk.CTkButton(
            self.window, text="", image=self.add_img, command=lambda: GUI_Condition(self.window, self.controller, "add"), width=20, height=20, fg_color="transparent"
        )
        self.add_condition_button.place(x=317, y=176)

        self.edit_condition_button = ctk.CTkButton(
            self.window, text="", image=self.edit_img, command=self.modify_condition, width=20, height=20, fg_color="transparent"
        )
        self.edit_condition_button.place(x=349, y=182)

    def update_dropdown_condition(self, options):
        if not options:
            options = ["No existen condiciones."]
    
        self.dropdown_cond = ctk.CTkOptionMenu(self.window, values=options,
                                               width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                               text_color=self.color_aux)
        self.dropdown_cond.set("Seleccionar")
        self.dropdown_cond.place(x=106, y=182)

    def update_dropdown_equation(self, options):
        if not options:
            options = ["No existen ecuaciones."]
        self.dropdown_eq = ctk.CTkOptionMenu(self.window, values=options,
                                             width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                             text_color=self.color_aux)
        self.dropdown_eq.set("Seleccionar")
        self.dropdown_eq.place(x=104, y=136)

    def update_dropdown_lang(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_lang = ctk.CTkOptionMenu(self.window, values=options, command=self.controller.set_language,
                                               width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                               text_color=self.color_aux)
        self.dropdown_lang.set(selected_option or "Seleccionar")
        self.dropdown_lang.place(x=104, y=26)

    def update_dropdown_output(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_output = ctk.CTkOptionMenu(self.window, values=options, command=self.controller.set_output,
                                                 width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                 text_color=self.color_aux)
        self.dropdown_output.set(selected_option or "Seleccionar")
        self.dropdown_output.place(x=104, y=58)

    def update_dropdown_method(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_method = ctk.CTkOptionMenu(self.window, values=options, command=self.controller.set_method,
                                                 width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                 text_color=self.color_aux)
        self.dropdown_method.set(selected_option or "Seleccionar")
        self.dropdown_method.place(x=104, y=97)

    def modify_equation(self):
        selected = self.dropdown_eq.get()
        if selected != "Seleccionar":
            GUI_Equation(self.window, self.controller, "edit", selected)

    def modify_condition(self):
        selected = self.dropdown_cond.get()
        if selected != "Seleccionar":
            GUI_Condition(self.window, self.controller, "edit", selected)

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