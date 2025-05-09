import customtkinter as ctk
from customtkinter import CTkImage 
from tkinter import Menu, filedialog
from PIL import Image , ImageFont
import os
import sys
from .equation_view_ckt import GUI_Equation
from .condition_view import GUI_Condition
from .simulation_view import GUI_Simulation
import tkinter as tk


#0,48671875
#0,52375
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
        
        #Obtenemos la resolución de la pantalla
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana raíz temporal
        self.screen_width =int(root.winfo_screenwidth()* 0.48671875)
        self.screen_height =int(root.winfo_screenheight()* 0.52375)
        root.destroy()  # Destruir la ventana raíz después de obtener la resolución

        self.window = ctk.CTk()
        self.window.geometry(f"{self.screen_width}x{int(self.screen_height)}")
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
        # self.window_dash()
    
        #Añadir panel de errores
        self.error_frame = ctk.CTkFrame(self.window, fg_color="#FFFFFF", corner_radius=18, height=25)
        self.error_frame.pack(side="bottom", anchor="s", fill="x",pady=15, padx=15)

        self.top_menu()

        self.aux_frame_max_width = 400
        self.frame_open = False
        self.aux_frame = ctk.CTkFrame(self.window, corner_radius=15, width=0, height= 250)
        self.aux_frame.pack(side="right", anchor="e", fill="y",padx=10, pady=10)

        self.create_main_frame()
        self.button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.button_frame.pack(side="bottom", anchor="center", fill="x")

        self.generate_button = ctk.CTkButton(
            self.button_frame, text="Generar", command=self.generate_program, width=100, height=40
   
        )
        self.generate_button.pack(side="left", padx=15 ,pady=10)

        self.simulate_button = ctk.CTkButton(
            self.button_frame, text="Simular", command=self.init_sim_view, width=100, height=40, 
            text_color=self.color_aux, fg_color=self.color_button_drop, hover_color="#0A4F7D", state="disabled"
        )
        self.simulate_button.pack(side="left", padx=10 ,pady=10)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        self.main_frame.pack(anchor="center", fill="x", padx=15, pady=15, expand=True)
       
        self.language_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400, height= 250)
        self.create_label(self.language_frame,"Lenguaje","left")
        options = list(self.controller.get_list_languages())
        self.update_dropdown_lang(options)
        self.language_frame.pack(side="top", anchor="w", fill="x", padx=5, pady=5)

        self.output_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400, height= 250)
        self.create_label(self.output_frame,"Salida", "left")
        options = list(self.controller.get_list_output())
        self.update_dropdown_output(options)
        self.output_frame.pack(side="top", anchor="w", fill="x", padx=5, pady=5)

        self.method_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400, height= 250)
        self.create_label(self.method_frame,"Método Integración","left")
        options = list(self.controller.get_list_methods())
        self.update_dropdown_method(options)
        self.method_frame.pack(side="top", anchor="w", fill="x", padx=5, pady=5)
       
        self.equation_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400, height= 250)
        self.widget_equation()
        self.equation_frame.pack(side="top", anchor="w", fill="x", padx=5, pady=5)
       
        self.condition_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=400, height= 250)
        self.widget_condition()    
        self.condition_frame.pack(side="top", anchor="w", fill="x",padx=5, pady=5)

    
    def create_label(self, father, text, side):
        label = ctk.CTkLabel(father, text=text, text_color=self.color_text, anchor="w", justify="left")
        label.pack(side=side, anchor="w", padx=5, pady=5)

    def window_dash(self):
        self.top_bar = ctk.CTkFrame(self.window,width=10, height=200, fg_color=self.color_window, corner_radius=0)
        self.top_bar.pack(side="top",fill="x")
        self.top_bar.bind("<Button-1>", self.start_move)
        self.top_bar.bind("<B1-Motion>", self.do_move)

        # Botón de cerrar
        self.close_button = ctk.CTkButton(self.top_bar, text="x" ,fg_color="red", width=5, height=5, command=self.window.destroy, corner_radius=2.5) 
        self.close_button.pack(side="right", anchor="center", padx=10, pady=5)

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
        self.create_label(self.equation_frame,"Ecuaciones","left")
       
        self.edit_equation_button = ctk.CTkButton(
            self.equation_frame, 
            text="", 
            image=self.edit_img, 
            command=lambda: self.toggle_frame("edit", self.dropdown_eq.get()),   
            width=20, height=20, 
            fg_color="transparent"
        )
        self.edit_equation_button.pack(side="right", anchor="w", padx=5, pady=5)

        self.add_equation_button = ctk.CTkButton(
            self.equation_frame, 
            text="", 
            image=self.add_img, 
            command=lambda: self.toggle_frame("add"), 
            width=20, height=20, 
            fg_color="transparent"
        )
        self.add_equation_button.pack(side="right", anchor="w", padx=5, pady=5)

        self.update_dropdown_equation(self.controller.get_list_equations())

    def widget_condition(self):
        self.create_label(self.condition_frame,"Condiciones","left")
        
        self.edit_condition_button = ctk.CTkButton(
            self.condition_frame, text="", image=self.edit_img, command=self.modify_condition, width=20, height=20, fg_color="transparent"
        )
        self.edit_condition_button.pack(side="right", anchor="w", padx=5, pady=5)

        self.add_condition_button = ctk.CTkButton(
            self.condition_frame, text="", image=self.add_img, command=lambda: GUI_Condition(self.window, self.controller, "add"), width=20, height=20, fg_color="transparent"
        )
        self.add_condition_button.pack(side="right", anchor="w", padx=5, pady=5)

        self.update_dropdown_condition(self.controller.get_list_conditions())
       
    def update_dropdown_condition(self, options):
        if not options:
                options = ["No existen condiciones."]

        if not hasattr(self, 'dropdown_cond'):
            self.dropdown_cond = ctk.CTkOptionMenu(self.condition_frame, values=options,
                                                width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                text_color=self.color_aux)
            self.dropdown_cond.set("Seleccionar")
            self.dropdown_cond.pack(side="right", anchor="w", padx=5, pady=5)
        else:
            self.dropdown_cond.configure(values=options)

            if not self.dropdown_cond.winfo_ismapped():
                self.dropdown_cond.pack(side="right", anchor="w", padx=5, pady=5)

    def update_dropdown_equation(self, options):
        if not options:
                options = ["No existen ecuaciones."]
        
        if not hasattr(self, 'dropdown_eq'):
            self.dropdown_eq = ctk.CTkOptionMenu(self.equation_frame, values=options,
                                                width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                text_color=self.color_aux)
            self.dropdown_eq.set("Seleccionar")
            self.dropdown_eq.pack(side="right", anchor="w", padx=5, pady=5)
            self.dropdown_eq.pack(side="right", anchor="w", padx=5, pady=5)

        else:
            self.dropdown_eq.configure(values=options)
            
            if not self.dropdown_eq.winfo_ismapped():
                self.dropdown_eq.pack(side="right", anchor="w", padx=5, pady=5)
            
    def update_dropdown_lang(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]
        
        if not hasattr(self, 'dropdown_lang'):
            self.dropdown_lang = ctk.CTkOptionMenu(self.language_frame, values=options, command=self.controller.set_language,
                                                width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                text_color=self.color_aux)
            self.dropdown_lang.set(selected_option or "Seleccionar")
            self.dropdown_lang.pack(side="right", anchor="w", padx=5, pady=5)

        else:
            self.dropdown_lang.configure(values=options)
            if selected_option:
                self.dropdown_lang.set(selected_option)
            else:
                self.dropdown_lang.set("Seleccionar")

    def update_dropdown_output(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]

        if not hasattr(self, 'dropdown_output'):
            self.dropdown_output = ctk.CTkOptionMenu(self.output_frame, values=options, command=self.controller.set_output,
                                                    width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                    text_color=self.color_aux)
            self.dropdown_output.set(selected_option or "Seleccionar")
            self.dropdown_output.pack(side="right", anchor="w", padx=5, pady=5)
        else:
            self.dropdown_output.configure(values=options)
            if selected_option:
                self.dropdown_output.set(selected_option)
            else:
                self.dropdown_output.set("Seleccionar")

    def update_dropdown_method(self, options, selected_option=None):
        options = list(options) or ["Seleccionar"]

        if not hasattr(self, 'dropdown_method'):
            self.dropdown_method = ctk.CTkOptionMenu(self.method_frame, values=options, command=self.controller.set_method,
                                                    width=198, height=20, fg_color=self.color_dropdown, button_color=self.color_button_drop,
                                                    text_color=self.color_aux)
            self.dropdown_method.set(selected_option or "Seleccionar")
            self.dropdown_method.pack(side="right", anchor="w", padx=5, pady=5)
        else:
            self.dropdown_method.configure(values=options)
            if selected_option:
                self.dropdown_method.set(selected_option)
            else:
                self.dropdown_method.set("Seleccionar")

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

    def toggle_frame(self, option=None, selected=None):
        
        if self.frame_open:
            print("Cerrando frame")
            self.hide_frame(self.aux_frame.winfo_width())
            self.update_dropdown_condition(self.controller.get_list_conditions())
            self.update_dropdown_equation(self.controller.get_list_equations())
            self.update_dropdown_lang(self.controller.get_list_languages())
            self.update_dropdown_output(self.controller.get_list_output())
            self.update_dropdown_method(self.controller.get_list_methods())
            
            if hasattr(self, 'eq_frm'):
                self.eq_frm.delete()
                del self.eq_frm

        else:
            print("Abriendo frame")
            self.show_frame(self.aux_frame.winfo_width())
            self.dropdown_cond.pack_forget()
            self.dropdown_eq.pack_forget()
            self.dropdown_lang.pack_forget()
            self.dropdown_output.pack_forget()
            self.dropdown_method.pack_forget()
            self.add_condition_button.pack_forget()
            self.edit_condition_button.pack_forget()
            self.add_equation_button.pack_forget()
            self.edit_equation_button.pack_forget()
            self.eq_frm=GUI_Equation(self.aux_frame, self.controller, option, selected)
            
            

    def show_frame(self,width):
        """Animar la aparición del frame."""
        
        if width < self.aux_frame_max_width:
            new_width = width + 20
            self.aux_frame.configure(width=new_width)
            # self.window.update_idletasks()
            self.window.after(10, self.show_frame, new_width)
        else:
            self.frame_open = True

    def hide_frame(self,width):
        """Animar la desaparición del frame."""

        if width > self.aux_frame_max_width:
            width = self.aux_frame_max_width

        if width > 1:
            new_width = width - 20
            self.aux_frame.configure(width=new_width)
            # self.window.update_idletasks()
            self.window.after(10, self.hide_frame,new_width)
        else:
            self.frame_open = False

    def run(self):
        self.window.mainloop()