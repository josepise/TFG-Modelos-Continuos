import tkinter as tk
from tkinter import scrolledtext, Menu

class GeneratorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Generador de Programas de Simulación Continua")
        self.root.geometry("800x600")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # Create the menu bar
        self.menu_bar = Menu(self.root)

        # Create "Archivo" menu
        archivo_menu = Menu(self.menu_bar, tearoff=0)
        # archivo_menu.add_command(label="Nuevo", command=self.controller.new_file)
        # archivo_menu.add_command(label="Abrir", command=self.controller.open_file)
        # archivo_menu.add_command(label="Guardar", command=self.controller.save_file)
        # archivo_menu.add_separator()
        # archivo_menu.add_command(label="Salir", command=self.root.quit)
        # self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

        # # Create "Ver" menu
        # ver_menu = Menu(self.menu_bar, tearoff=0)
        # ver_menu.add_command(label="Pantalla Completa", command=self.controller.toggle_fullscreen)
        # ver_menu.add_command(label="Restaurar Tamaño", command=self.controller.restore_size)
        # self.menu_bar.add_cascade(label="Ver", menu=ver_menu)

        # # Attach the menu bar to the root window
        # self.root.config(menu=self.menu_bar)

        # Create "Archivo" menu
        archivo_menu = Menu(self.menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo")
        archivo_menu.add_command(label="Abrir")
        archivo_menu.add_command(label="Guardar")
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir")
        self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

        # Create "Ver" menu
        ver_menu = Menu(self.menu_bar, tearoff=0)
        ver_menu.add_command(label="Pantalla Completa")
        ver_menu.add_command(label="Restaurar Tamaño")
        self.menu_bar.add_cascade(label="Ver", menu=ver_menu)

        # Attach the menu bar to the root window
        self.root.config(menu=self.menu_bar)

    def create_widgets(self):
        # Create a frame for input fields
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Create a label and entry for the simulation file name
        tk.Label(self.input_frame, text="Nombre del archivo de simulación:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_name_entry = tk.Entry(self.input_frame, width=50)
        self.file_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create a label and dropdown menu for equations
        tk.Label(self.input_frame, text="Ecuaciones:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)

        # Create a StringVar to hold the selected equation
        self.selected_equation = tk.StringVar(self.input_frame)
        self.selected_equation.set("Selecciona una ecuación")  # Default value

        # Create a dropdown menu with equations from the model
        self.equations_dropdown = tk.OptionMenu(self.input_frame, self.selected_equation, *self.controller.get_equations())
        self.equations_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Create buttons to add, edit, and delete equations
        self.add_equation_button = tk.Button(self.input_frame, text="Añadir", command=self.add_equation)
        self.add_equation_button.grid(row=1, column=2, padx=5, pady=5)

        self.edit_equation_button = tk.Button(self.input_frame, text="Editar", command=self.edit_equation)
        self.edit_equation_button.grid(row=1, column=3, padx=5, pady=5)

        self.delete_equation_button = tk.Button(self.input_frame, text="Eliminar", command=self.delete_equation)
        self.delete_equation_button.grid(row=1, column=4, padx=5, pady=5)

        # Create a label and text area for conditions
        tk.Label(self.input_frame, text="Condiciones:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.conditions_text = scrolledtext.ScrolledText(self.input_frame, width=60, height=10)
        self.conditions_text.grid(row=2, column=1, padx=5, pady=5)

        # Create a frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # # Add buttons for actions
        self.generate_button = tk.Button(self.button_frame, text="Generar Simulación", command=self.controller.generate_simulation)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Limpiar", command=self.controller.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Salir", command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=5)

        # Add buttons for actions without commands
        self.generate_button = tk.Button(self.button_frame, text="Generar Simulación")
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Limpiar")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Salir")
        self.exit_button.pack(side=tk.RIGHT, padx=5)

    def add_equation(self):
        # Get the selected equation from the dropdown menu
        selected_equation = self.selected_equation.get()
        # Add the equation to the model (controller)
        self.controller.add_equation(selected_equation)

    def edit_equation(self):
        # Get the selected equation from the dropdown menu
        selected_equation = self.selected_equation.get()
        # Edit the equation in the model (controller)
        self.controller.edit_equation(selected_equation)
    
    def delete_equation(self):
        # Get the selected equation from the dropdown menu
        selected_equation = self.selected_equation.get()
        # Delete the equation from the model (controller)
        self.controller.delete_equation(selected_equation)

    def get_equation_names(self):
        # Get the names of the equations from the model (controller)
        return self.controller.get_equation_names()

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneratorView(root, None)  # Pass a controller instance here
    root.mainloop()