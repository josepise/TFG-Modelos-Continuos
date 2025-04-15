from pathlib import Path
from tkinter import Toplevel, Button, Entry, Tk, Canvas
from tkinter import StringVar, OptionMenu, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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


    def create_widgets(self):
        
        self.widget_equation()

        self.canvas.create_text(
            10.0,
            179.0,
            anchor="nw",
            text="Condiciones",
            fill="#FFFFFF",
            font=("Inter", 14 * -1)
        )

        self.canvas.create_rectangle(
            104.0,
            176.0,
            302.0,
            196.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_rectangle(
            317.0,
            176.0,
            337.0,
            196.0,
            fill="#D9D9D9",
            outline=""
        )

        self.canvas.create_rectangle(
            349.0,
            176.0,
            369.0,
            196.0,
            fill="#D9D9D9",
            outline=""
        )
       
        self.canvas.create_rectangle(
            659.0,
            399.0,
            784.0,
            449.0,
            fill="#D9D9D9",
            outline=""
        )

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


    def update_dropdown_equation(self, options):
        self.dropdown_var = StringVar(self.window)
        self.dropdown_var.set("Seleccionar")  # Default value
        
        if not options:  # Ensure there is at least one default option
            options = ["No existen ecuaciones"]

        self.dropdown_menu = OptionMenu(
            self.window,
            self.dropdown_var,
            *options
        )
        self.dropdown_menu.place(x=104.0, y=136.0, width=198.0, height=20.0)

    def modify_equation(self):
        selected_equation = self.dropdown_var.get()
        if selected_equation != "Seleccionar":
            GUI_Equation(self.window, self.controler, "edit", selected_equation)
        else:
            print("No equation selected")            
            
    def run(self):
        self.window.mainloop()


class GUI_Equation(Toplevel):

    def __init__(self, parent, controller, mode="add", selected=None):
        super().__init__(parent)
        self.controler = controller
        self.mode = mode

        if mode == "add":
            self.title("Añadir ecuación")
        elif mode == "edit":
            self.title("Editar ecuación")


        self.geometry("650x268")
        self.configure(bg = "#959494")

        canvas = Canvas(
            self,
            bg = "#959494",
            height = 268,
            width = 650,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        
        canvas.create_text(
            46.0,
            20.0,
            anchor="nw",
            text="Ecuación",
            fill="#FFFFFF",
            font=("Inter", 12 * -1)
        )

        self.text_entry_equation_window = Entry(self)
        self.text_entry_equation_window.place(x=110.0, y=16.0, width=326.0, height=23.0)

        canvas.create_text(
            46.0,
            56.0,
            anchor="nw",
            text="Variables",
            fill="#FFFFFF",
            font=("Inter", 12 * -1)
        )

        self.text_entry_var = Entry(self)
        self.text_entry_var.place(x=110.0, y=52.0, width=326.0, height=23.0)

        canvas.create_text(
            32.0,
            92.0,
            anchor="nw",
            text="Constantes",
            fill="#FFFFFF",
            font=("Inter", 12 * -1)
        )

        self.text_entry_constants = Entry(self)
        self.text_entry_constants.place(x=110.0, y=88.0, width=326.0, height=23.0)

        self.plot_text_equation(self)
        
        if selected:
            self.selected=selected
            self.load_data()

        #Boton de añadir ecuacion
        if mode == "add":
            label = "Añadir"
            comando =lambda:self.add_equation(self.text_entry_equation_window.get(), 
                                                       self.text_entry_var.get(),    
                                                       self.text_entry_constants.get(),
                                                       self) 
        elif mode == "edit":
            label = "Editar"
            comando = lambda: self.edit_equation(self.text_entry_equation_window.get(), 
                                                        self.text_entry_var.get(),         
                                                        self.text_entry_constants.get(),
                                                        self)
            
        add_edit_button = Button(
            self,
            text=label,
            command=comando 
        )
        add_edit_button.place(x=506.0, y=218.0, width=129.0, height=36.0)

        canvas.create_rectangle(
            571.0,
            22.0,
            619.0,
            70.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            571.0,
            22.0,
            619.0,
            70.0,
            fill="#000000",
            outline="")

    def add_equation(self,text_equation,text_var, text_constants, window):
        self.controler.add_equation(text_equation,text_var,text_constants)
        window.destroy()

    def edit_equation(self,text_equation,text_var, text_constants, window):
        self.controler.edit_equation(text_equation,text_var,text_constants,self.selected)
        window.destroy()

    def load_data(self):
        str_eq, list_sym, list_const=self.controler.get_equation(self.selected)

        #Cargamos la ecuación en el cuadro de texto
        self.text_entry_equation_window.delete(0, "end")
        self.text_entry_equation_window.insert(0, str_eq)

        #Cargamos las variables en el cuadro de texto
        self.text_entry_var.delete(0, "end")
        self.text_entry_var.insert(0, list_sym)

        #Cargamos las constantes en el cuadro de texto
        self.text_entry_constants.delete(0, "end")
        self.text_entry_constants.insert(0, list_const)

        self.update_latex_display()
        

    def plot_text_equation(self, window):
        # Crear figura y ejes
        self.latex_fig = Figure(figsize=(5, 2), dpi=100)
        self.latex_ax = self.latex_fig.add_subplot(111)
        self.latex_ax.axis('off')

        # Crear el lienzo de matplotlib dentro de tkinter
        self.latex_canvas = FigureCanvasTkAgg(self.latex_fig, master=window)
        self.latex_canvas.draw()
        self.latex_canvas.get_tk_widget().place(x=22.0, y=134.0, width=414.0, height=120.0)

        # Vincular actualización en tiempo real
        self.text_entry_equation_window.bind(
            "<KeyRelease>",
            lambda event: self.update_latex_display()
        )

        # Mostrar contenido inicial
        self.update_latex_display()


    def update_latex_display(self):
        # Limpiar los ejes
        self.latex_ax.clear()
        self.latex_ax.axis('off')

        # Obtener el texto del Entry y convertirlo a LaTeX
        try:
            latex_string = sp.latex(sp.sympify(self.text_entry_equation_window.get()))
        except:
            latex_string = self.text_entry_equation_window.get()

        # Dibujar el texto
        if latex_string.strip():
            self.latex_ax.text(0.5, 0.5, f"${latex_string}$", fontsize=12, ha='center', va='center')
        else:
            self.latex_ax.text(0.5, 0.5, "", fontsize=12, ha='center', va='center', color='red')

        # Redibujar
        self.latex_canvas.draw()
