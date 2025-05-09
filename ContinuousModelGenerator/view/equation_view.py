from tkinter import Button, Canvas, Entry, Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

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
        self.configure(bg = "#92A6C0")

        canvas = Canvas(
            self,
            bg = "#92A6C0",
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

        #Boton de añadir/editar ecuacion
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

