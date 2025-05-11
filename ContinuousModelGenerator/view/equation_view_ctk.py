
from tkinter import Frame, Button, Canvas, Entry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import customtkinter as ctk

class GUI_Equation():
    def __init__(self, parent_frame, controller, mode="add", selected=None):
        self.parent_frame = parent_frame
        self.controler = controller
        self.mode = mode

        # Colores de la interfaz
        self.color_window = "#031240"
        self.color_bg = "#352F6B"
        self.color_text = "#3B52D9"
        self.color_button_drop = "#233559"
        self.color_dropdown = "#F2F2F2"
        self.color_aux = "#4A6DD9"

        # Limpiar el frame antes de crear nuevos elementos
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
            
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent", corner_radius=18)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame para los campos de entrada
        input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=10)
        input_frame.pack(side="top", fill="x", pady=5)

        # Etiqueta "Ecuación"
        equation_label = ctk.CTkLabel(input_frame, text="Ecuación",fg_color="transparent", 
                                      text_color=self.color_text)
        equation_label.pack(side="top", fill="x", padx=10, pady=2)

        # Entry para la ecuación
        self.text_entry_equation_window = ctk.CTkEntry(input_frame,border_width=2, 
                                                       border_color=self.color_bg)
        self.text_entry_equation_window.pack(side="top", fill="x", padx=10, pady=2)

        # Etiqueta "Variables"
        variables_label = ctk.CTkLabel(input_frame, text="Variables", fg_color="transparent", 
                                       text_color=self.color_text)
        variables_label.pack(side="top", fill="x", padx=10, pady=2)

        # Entry para las variables
        self.text_entry_var = ctk.CTkEntry(input_frame, border_width=2, border_color=self.color_bg)
        self.text_entry_var.pack(side="top", fill="x", padx=10, pady=2)

        # Etiqueta "Constantes"
        constants_label = ctk.CTkLabel(input_frame, text="Constantes", fg_color="transparent", 
                                       text_color=self.color_text)
        constants_label.pack(side="top", fill="x", padx=10, pady=2)

        # Entry para las constantes
        self.text_entry_constants = ctk.CTkEntry(input_frame, border_width=2, border_color=self.color_bg)
        self.text_entry_constants.pack(side="top", fill="x", padx=10, pady=2)

        # Frame para el canvas de LaTeX
        latex_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="white", border_width=2, 
                                   border_color=self.color_bg)
        latex_frame.pack(side="top", fill="both", expand=True, padx=10,pady=10)

        # Dibujar ecuación LaTeX
        self.plot_text_equation(latex_frame)

        # Frame para los botones
        button_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        button_frame.pack(side="bottom", fill="x", pady=10)

        # Botón de añadir/editar ecuación
        label = "Añadir" if self.mode == "add" else "Editar"
        if self.mode == "add":
            command = lambda: self.add_equation(
                self.text_entry_equation_window.get(),
                self.text_entry_var.get(),
                self.text_entry_constants.get()
            )
        else:
            command = lambda: self.edit_equation(
                self.text_entry_equation_window.get(),
                self.text_entry_var.get(),
                self.text_entry_constants.get()
            )

        self.add_edit_button = ctk.CTkButton(
            button_frame,
            text=label,
            command=command,
            corner_radius=8,
            fg_color=self.color_aux,
            text_color="#FFFFFF"
        )
        self.add_edit_button.pack(side="right", padx=10, pady=5)

        # Cargar datos si se está en modo edición
        if selected:
            self.selected = selected
            self.load_data()

    def add_equation(self, text_equation, text_var, text_constants):
        self.controler.add_equation(text_equation, text_var, text_constants)
        self.controler.toggle_frame()
        self.clear_entries()

    def edit_equation(self, text_equation, text_var, text_constants):
        self.controler.edit_equation(text_equation, text_var, text_constants, self.selected)
        self.controler.toggle_frame()
        self.clear_entries()

    def load_data(self):
        str_eq, list_sym, list_const = self.controler.get_equation(self.selected)

        # Cargar la ecuación en el Entry
        self.text_entry_equation_window.delete(0, "end")
        self.text_entry_equation_window.insert(0, str_eq)

        # Cargar las variables en el Entry
        self.text_entry_var.delete(0, "end")
        self.text_entry_var.insert(0, list_sym)

        # Cargar las constantes en el Entry
        self.text_entry_constants.delete(0, "end")
        self.text_entry_constants.insert(0, list_const)

        self.update_latex_display()

    def plot_text_equation(self, parent_frame):
        """Crea el canvas para renderizar la ecuación en LaTeX."""
        self.latex_fig = Figure(figsize=(5, 2), dpi=100)
        self.latex_ax = self.latex_fig.add_subplot(111)
        self.latex_ax.axis('off')

        self.latex_canvas = FigureCanvasTkAgg(self.latex_fig, master=parent_frame)
        self.latex_canvas.draw()
        self.latex_canvas.get_tk_widget().pack(anchor="center",fill="x",padx=10, pady=10)

        # Vincular actualización del LaTeX en tiempo real
        self.text_entry_equation_window.bind(
            "<KeyRelease>",
            lambda event: self.update_latex_display()
        )

        # Mostrar contenido inicial
        self.update_latex_display()

    def update_latex_display(self):
        """Actualiza el renderizado de la ecuación LaTeX."""
        self.latex_ax.clear()
        self.latex_ax.axis('off')

        try:
            latex_string = sp.latex(sp.sympify(self.text_entry_equation_window.get()))
        except:
            latex_string = self.text_entry_equation_window.get()

        if latex_string.strip():
            self.latex_ax.text(0.5, 0.5, f"${latex_string}$", fontsize=12, ha='center', va='center')
        else:
            self.latex_ax.text(0.5, 0.5, "", fontsize=12, ha='center', va='center', color='red')

        self.latex_canvas.draw()

    def clear_entries(self):
        """Limpia los campos de entrada."""
        self.text_entry_equation_window.delete(0, "end")
        self.text_entry_var.delete(0, "end")
        self.text_entry_constants.delete(0, "end")

    def delete(self):
        """Elimina el frame de la interfaz."""
        self.main_container.pack_forget()