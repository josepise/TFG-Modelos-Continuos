import customtkinter as ctk
from customtkinter import CTkImage 
from tkinter import Menu, filedialog
from PIL import Image , ImageFont
import os
import sys
from .equation_view import GUI_Equation
from .condition_view import GUI_Condition
from .simulation_view import GUI_Simulation
import tkinter as tk



class GUI_CTK:
    def __init__(self, controller=None):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.route_img = os.path.join("ContinuousModelGenerator", "resources", "img")
        self.controller = controller
        #ECEDF1
        # Colores de la interfaz
        self.color_window = "#031240"
        self.color_bg = "#352F6B"
        self.color_text = "#3B52D9"
        self.color_button_drop = "#233559"
        self.color_dropdown = "#F2F2F2"
        self.color_aux = "#4A6DD9"
        
        
        
        self.window = ctk.CTk()
        self.window.geometry("500x450")
        self.window.configure(fg_color=self.color_bg)
        # self.window.resizable(False, False)
        # self.window.overrideredirect(True)

        self.load_imgs()
        self.create_widgets()

    def init_sim_view(self):
        self.simulation_view = GUI_Simulation(self.window, self.controller)


    def get_simulation_view(self):
        return self.simulation_view
    
    def resource_path(self,relative_path):
        """ Obtiene la ruta del recurso, compatible con PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            # Cuando se ejecuta el .exe
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def load_imgs(self):
        self.add_img = CTkImage(light_image=Image.open(self.resource_path("ContinuousModelGenerator/resources/img/add.png")), size=(20, 20))
        self.edit_img = CTkImage(light_image=Image.open(self.resource_path("ContinuousModelGenerator/resources/img/edit.png")), size=(20, 20))
        

    def create_widgets(self):
        self.window_dash()
    
        #Añadir panel de errores
        self.error_frame = ctk.CTkFrame(self.window, fg_color="#FFFFFF", corner_radius=18, height=25)
        self.error_frame.pack(side="bottom", anchor="s", fill="x",pady=0, padx=0)

        self.top_menu()

        self.aux_frame = ctk.CTkFrame(self.window,fg_color=("white10", "white80"), corner_radius=15, width=400, height= 250)
        self.aux_frame.pack(side="right", anchor="e",fill="y", padx=10, pady=10)

        
        self.main_frame = ctk.CTkFrame(self.window, width=400, height= 250, corner_radius=15)
        self.main_frame.pack(anchor="center", padx=10, pady=10)
       
        self.create_label(self.main_frame,"Lenguaje", 23, 26)
        options = list(self.controller.get_list_languages())
        self.update_dropdown_lang(options)

        self.create_label(self.main_frame,"Salida", 23, 58)
        options = list(self.controller.get_list_output())
        self.update_dropdown_output(options)

        self.create_label(self.main_frame,"Método\nIntegración", 23, 97)
        options = list(self.controller.get_list_methods())
        self.update_dropdown_method(options)

        self.widget_equation()
        self.widget_condition()
        
        self.bottom_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", anchor="nw", fill="x", padx=5, pady=5)

        self.button_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.button_frame.pack(side="top", anchor="e", fill="x")

        self.generate_button = ctk.CTkButton(
            self.button_frame, text="Generar", command=self.generate_program, width=100, height=40
        )
        self.generate_button.pack(side="left", padx=10 ,pady=10)

        self.simulate_button = ctk.CTkButton(
            self.button_frame, text="Simular", command=self.init_sim_view, width=100, height=40, 
            text_color=self.color_aux, fg_color=self.color_button_drop, hover_color="#0A4F7D", state="disabled"
        )
        self.simulate_button.pack(side="left", padx=10 ,pady=10)

        

    def create_label(self, father, text, x, y):
        label = ctk.CTkLabel(father, text=text, text_color=self.color_text, font=("Roboto", 12, "bold"), anchor="w", justify="left")
        label.place(x=x, y=y)

    def window_dash(self):
        self.top_bar = ctk.CTkFrame(self.window,width=10, height=200, fg_color=self.color_window, corner_radius=0)
        self.top_bar.pack(side="top",fill="x")
        self.top_bar.bind("<Button-1>", self.start_move)
        self.top_bar.bind("<B1-Motion>", self.do_move)

        # Botón de cerrar
        self.close_button = ctk.CTkButton(self.top_bar, text="x", width=5, height=5, command=self.window.destroy, corner_radius=5) 
        self.close_button.pack(side="right", padx=10, pady=5)

        # Botón de minimizar
        self.minimize_button = ctk.CTkButton(self.top_bar, text="_", width=5, height=5, command=self.window.iconify, corner_radius=5)
        self.minimize_button.pack(side="right", padx=5, pady=5)

        #Label transparente para aumentar la altura de la barra
        self.label = ctk.CTkLabel(self.top_bar, text="", width=10, height=10, fg_color="transparent")
        self.label.pack(side="top", padx=5)

    
    def top_menu(self):
        self.menu_frame = ctk.CTkFrame(self.window, fg_color="transparent", height=60)
        self.menu_frame.pack(side="top", fill="x")
        self.init_file_menu()

        # Segmentado menu
        self.segmented_menu_var = ctk.StringVar(value="📁 Archivo")
        self.segmented_menu = ctk.CTkSegmentedButton(
            self.menu_frame,
            values=["📁 Archivo", "🔍 Ver", "❓ Ayuda"],
            command=self.handle_segmented_menu,
            variable=self.segmented_menu_var
        )
        self.segmented_menu.pack(side="left",anchor="w", padx=5, pady=5)

        # function = lambda event: self.handle_segmented_menu(self.segmented_menu_var.get())
        # for child in self.segmented_menu.winfo_children():
        #     child.bind("<Button-1>", function)

    def handle_segmented_menu(self, value):
        if value == "📁 Archivo":
            pass
            # height = self.file_menu_segmented.winfo_height()
            # if height > 1:
            #     self.hide_menu(self.file_menu_segmented, height)
            # else:
            #     self.show_menu(self.file_menu_segmented, height)
        # elif value == "🔍 Ver":
        #     if hasattr(self, 'file_menu_segmented'):
        #         self.file_menu_segmented.destroy()
        #         del self.file_menu_segmented
        # elif value == "❓ Ayuda":
        #     if hasattr(self, 'file_menu_segmented'):
        #         self.file_menu_segmented.destroy()
        #         del self.file_menu_segmented
         

    def init_file_menu(self):

        self.file_menu_var = ctk.StringVar()
        self.file_menu_segmented = ctk.CTkSegmentedButton(
            self.menu_frame,
            values=["🆕 Nuevo ", "📂 Abrir", "💾 Guardar", "❌ Salir"],
            command=self.handle_file_menu_action,
            variable=self.file_menu_var
        )
        self.file_menu_segmented.pack(side="right",anchor="center",padx=5, pady=5)

        self.hide_menu(self.file_menu_segmented, self.file_menu_segmented.winfo_height())

    def handle_file_menu_action(self, action):
        if action == "🆕 Nuevo":
            self.controller.new_file()
        elif action == "📂 Abrir":
            self.open_config_file()
        elif action == "💾 Guardar":
            self.save_config_file()
        elif action == "❌ Salir":
            self.window.destroy()

    def show_view_menu(self):
        self.view_menu_frame = ctk.CTkFrame(self.window, fg_color=self.color_dropdown, corner_radius=10)
        self.view_menu_frame.place(x=90, y=35)

        self.timeline_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            self.view_menu_frame, text="Mostrar líneas de tiempo", variable=self.timeline_var,
            fg_color="transparent", text_color=self.color_aux
        ).pack(anchor="w", padx=5, pady=2)

    def show_help_menu(self):
        self.help_menu_frame = ctk.CTkFrame(self.window, fg_color=self.color_dropdown, corner_radius=10)
        self.help_menu_frame.place(x=175, y=35)

        ctk.CTkButton(
            self.help_menu_frame, text="Ver Ayuda", width=100, height=30, fg_color="transparent",
            text_color=self.color_aux, hover_color="#D3D3D3"
        ).pack(anchor="w", padx=5, pady=2)


    def widget_equation(self):
        self.create_label(self.main_frame,"Ecuaciones", 23, 139)
        self.update_dropdown_equation(self.controller.get_list_equations())

        self.add_equation_button = ctk.CTkButton(
            self.main_frame, text="", image=self.add_img, command=lambda: GUI_Equation(self.window, self.controller, "add"), width=20, height=20, fg_color="transparent"
        )
        self.add_equation_button.place(x=317, y=136)

        self.edit_equation_button = ctk.CTkButton(
            self.main_frame, text="", image=self.edit_img, command=self.modify_equation, width=20, height=20, fg_color="transparent"
        )
        self.edit_equation_button.place(x=349, y=136)

    def widget_condition(self):
        self.create_label(self.main_frame,"Condiciones", 23, 179)
        self.update_dropdown_condition(self.controller.get_list_conditions())

        self.add_condition_button = ctk.CTkButton(
            self.main_frame, text="", image=self.add_img, command=lambda: GUI_Condition(self.window, self.controller, "add"), width=20, height=20, fg_color="transparent"
        )
        self.add_condition_button.place(x=317, y=176)

        self.edit_condition_button = ctk.CTkButton(
            self.main_frame, text="", image=self.edit_img, command=self.modify_condition, width=20, height=20, fg_color="transparent"
        )
        self.edit_condition_button.place(x=349, y=176)

    def update_dropdown_condition(self, options):
        if not options:
            options = ["No existen condiciones."]
    
        self.dropdown_cond = ctk.CTkOptionMenu(self.main_frame, values=options,
                                               width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                               text_color=self.color_aux)
        self.dropdown_cond.set("Seleccionar")
        self.dropdown_cond.place(x=106, y=182)

    def update_dropdown_equation(self, options):
        if not options:
            options = ["No existen ecuaciones."]
        self.dropdown_eq = ctk.CTkOptionMenu(self.main_frame, values=options,
                                             width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                             text_color=self.color_aux)
        self.dropdown_eq.set("Seleccionar")
        self.dropdown_eq.place(x=104, y=136)

    def update_dropdown_lang(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_lang = ctk.CTkOptionMenu(self.main_frame, values=options, command=self.controller.set_language,
                                               width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                               text_color=self.color_aux)
        self.dropdown_lang.set(selected_option or "Seleccionar")
        self.dropdown_lang.place(x=104, y=26)

    def update_dropdown_output(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_output = ctk.CTkOptionMenu(self.main_frame, values=options, command=self.controller.set_output,
                                                 width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                 text_color=self.color_aux)
        self.dropdown_output.set(selected_option or "Seleccionar")
        self.dropdown_output.place(x=104, y=58)

    def update_dropdown_method(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        self.dropdown_method = ctk.CTkOptionMenu(self.main_frame, values=options, command=self.controller.set_method,
                                                 width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                 text_color=self.color_aux)
        self.dropdown_method.set(selected_option or "Seleccionar")
        self.dropdown_method.place(x=104, y=97)

    def modify_equation(self):
        selected = self.dropdown_eq.get()
        if selected != "Seleccionar":
            GUI_Equation(self.main_frame, self.controller, "edit", selected)

    def modify_condition(self):
        selected = self.dropdown_cond.get()
        if selected != "Seleccionar":
            GUI_Condition(self.main_frame, self.controller, "edit", selected)

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

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
    
    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.offset_x
        y = self.window.winfo_pointery() - self.offset_y
        self.window.geometry(f"+{x}+{y}")

    def show_menu(self, menu, longitude):
        """Animar la aparición del menú deslizante."""
        if longitude < self.menu_width:
            new_width = longitude + 20
            menu.configure(width=new_width)
            self.window.after(10, self.show_menu,menu,new_width)
        else:
            print("Menu opened")
            self.menu_open = True

    def hide_menu(self, frame, longitude):
        """Animar la desaparición del menú deslizante."""
    
        if longitude > 1:
            new_width = longitude - 20
            frame.configure(height=new_width)
            self.window.after(10, self.hide_menu, frame, new_width)
        else:
            self.menu_open = False

    def run(self):
        self.window.mainloop()