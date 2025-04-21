from tkinter import Button, Tk, Canvas, Menu
from tkinter import StringVar, OptionMenu, PhotoImage
from .equation_view import GUI_Equation
from .condition_view import GUI_Condition
import sympy as sp
import os

class GUI:
    def __init__(self, controler=None):
        #Definimos la ruta de la carpeta de recursos de imágenes
        self.route_img = os.path.join("ContinuousModelGenerator","resources", "img")
        
        #Añadimos el controlador a la vista
        self.controler = controler

        self.window = Tk()
        self.window.geometry("811x468")
        self.window.configure(bg="#5C603B")
        self.window.resizable(False, False)

        self.canvas = Canvas(
            self.window,
            bg="#5C603B",
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
        self.update_dropdown_equation(self.controler.get_list_equations())

        self.add_equation_button = Button(
            self.window,
            text="Añadir",
            image=self.add_img,
            command=lambda: GUI_Equation(self.window, self.controler, "add"),
            borderwidth=0,
            background="#5C603B",
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
            background="#5C603B",
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

        self.update_dropdown_condition(self.controler.get_list_conditions())

        
        self.add_condition_button = Button(
            self.window,
            text="Añadir",
            image=self.add_img,
            command=lambda: GUI_Condition(self.window, self.controler, "add"),
            borderwidth=0,
            background="#5C603B",
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
            background="#5C603B",
            highlightthickness=0,
            relief="flat"
        )

        self.edit_condition_button.place(x=349.0, y=176.0, width=20.0, height=20.0)

    def create_widgets(self):
        
        self.top_menu()

        self.widget_equation()
        
        self.widget_condition()
        
        self.help_button = Button(
            self.window,
            text="Ayuda",
            command=lambda:self.controler.generate,  # Reemplazar con la acción deseada
            bg="#D9D9D9",
            relief="flat"
        )
        self.help_button.place(x=659.0, y=399.0, width=125.0, height=50.0)

        self.canvas.create_rectangle(
            250.0,
            30.0,
            372.0,
            54.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_text(
            264.0,
            33.0,
            anchor="nw",
            text="Ayuda",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        self.canvas.create_rectangle(
            125.0,
            30.0,
            247.0,
            54.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_text(
            139.0,
            33.0,
            anchor="nw",
            text="Ver",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        self.canvas.create_rectangle(
            0.0,
            30.0,
            122.0,
            54.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_text(
            14.0,
            33.0,
            anchor="nw",
            text="Archivo",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        self.canvas.create_rectangle(
            0.0,
            0.0,
            1440.0,
            27.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_text(
            12.0,
            7.0,
            anchor="nw",
            text="Generador de Programas de Simulación Continua",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

    def top_menu(self):
        menu_bar = Menu(self.window)

        menu_archivo = Menu(menu_bar, tearoff=0)
        menu_archivo.add_command(label="Nuevo")#, command=nuevo_archivo)
        menu_archivo.add_command(label="Abrir")#, command=abrir_archivo)
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

    def modify_equation(self):
        selected_equation = self.dropdown_eq.get()
        if selected_equation != "Seleccionar":
            GUI_Equation(self.window, self.controler, "edit", selected_equation)
        else:
            print("No equation selected")   

    def modify_condition(self):
        selected_condition = self.dropdown_cond.get()
        if selected_condition != "Seleccionar":
            GUI_Condition(self.window, self.controler, "edit", selected_condition)
        else:
            print("No condition selected")
    def run(self):
        self.window.mainloop()


