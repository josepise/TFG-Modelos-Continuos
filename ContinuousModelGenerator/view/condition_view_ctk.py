import customtkinter as ctk


class GUI_Condition:
    def __init__(self, parent_frame, controller, mode="add", selected=None):
        self.parent_frame = parent_frame
        self.controller = controller
        self.mode = mode

        # Colores de la interfaz
        self.color_window = "#031240"
        self.color_bg = "#352F6B"
        self.color_text = "#3B52D9"
        self.color_aux = "#4A6DD9"

        # Limpiar el frame antes de crear nuevos elementos
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent", corner_radius=18)
        self.main_container.pack(fill="both", padx=10, pady=10)

        # Frame para los campos de entrada
        input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=10)
        input_frame.pack(side="left", fill="x", pady=5)

        # Campo: Expresiones lógicas
        self.create_label(input_frame, "Expresiones lógicas")
        self.text_entry_condition = self.create_textbox(input_frame,50)

        # Campo: Acción
        self.create_label(input_frame, "Acción")
        self.text_entry_action = self.create_textbox(input_frame,50)

        # Campo: Variables
        self.create_label(input_frame, "Variables")
        self.text_entry_var = self.create_textbox(input_frame)

        # Campo: Constantes
        self.create_label(input_frame, "Constantes")
        self.text_entry_constants = self.create_textbox(input_frame)

        # Frame para la vista previa
        preview_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="white", border_width=2,
                                     border_color=self.color_bg)
        preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Vista previa
        self.text_preview = ctk.CTkTextbox(preview_frame, state="disabled", wrap="word", border_width=2,
                                           border_color=self.color_bg)
        self.text_preview.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame para los botones
        button_frame = ctk.CTkFrame(input_frame, corner_radius=10)
        button_frame.pack(side="left", fill="x", pady=10)

        # Botón de añadir/editar condición
        label = "Añadir" if self.mode == "add" else "Editar"
        command = self.get_command()
        self.add_edit_button = ctk.CTkButton(
            button_frame,
            text=label,
            command=command,
            corner_radius=8,
            fg_color=self.color_aux,
            text_color="#FFFFFF",
            width=10,
            height=30
        )
        self.add_edit_button.pack(side="right", padx=10, pady=5)

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.controller.toggle_frame,
            corner_radius=8,
            fg_color=self.color_aux,
            text_color="#FFFFFF",
            width=10,
            height=30
        )
        self.cancel_button.pack(side="left", padx=10, pady=5)
        

        # Cargar datos si se está en modo edición
        if selected:
            self.selected = selected
            self.load_data()
            self.preview_condition()

        # Vincular vista previa a los campos de entrada
        self.text_entry_condition.bind("<KeyRelease>", lambda event: self.preview_condition())
        self.text_entry_action.bind("<KeyRelease>", lambda event: self.preview_condition())

    def create_label(self, parent, text):
        """Crea una etiqueta."""
        label = ctk.CTkLabel(parent, text=text, fg_color="transparent", text_color=self.color_text)
        label.pack(side="top", fill="x", padx=10, pady=2)

    def create_textbox(self, parent, height=10):
        """Crea un cuadro de texto."""
        textbox = ctk.CTkTextbox(parent, wrap="word", border_width=2, border_color=self.color_bg,
                                 height=height)
        textbox.pack(side="top", fill="x", padx=10, pady=2)
        return textbox

    def get_command(self):
        """Obtiene el comando para añadir o editar."""
        if self.mode == "add":
            return lambda: self.add_condition(
                self.text_entry_condition.get("1.0", "end-1c"),
                self.text_entry_action.get("1.0", "end-1c"),
                self.text_entry_var.get("1.0", "end-1c"),
                self.text_entry_constants.get("1.0", "end-1c")
            )
        else:
            return lambda: self.edit_condition(
                self.text_entry_condition.get("1.0", "end-1c"),
                self.text_entry_action.get("1.0", "end-1c"),
                self.text_entry_var.get("1.0", "end-1c"),
                self.text_entry_constants.get("1.0", "end-1c")
            )

    def add_condition(self, text_logic_exp, text_action, text_var, text_constants):
        success=self.controller.add_condition(text_logic_exp, text_action, text_var, text_constants)
        
        if success: 
            self.controller.toggle_frame()

    def edit_condition(self, text_logic_exp, text_action, text_var, text_constants):
        success=self.controller.edit_condition(text_logic_exp, text_action, text_var, text_constants, self.selected)
        
        if success:
            self.controller.toggle_frame()

    def load_data(self):
        str_cond, str_act, list_sym, list_const = self.controller.get_condition(self.selected)

        self.text_entry_condition.insert("1.0", str_cond)
        self.text_entry_action.insert("1.0", str_act)
        self.text_entry_var.insert("1.0", list_sym)
        self.text_entry_constants.insert("1.0", list_const)

    def preview_condition(self):
        self.text_preview.configure(state="normal")
        self.text_preview.delete("1.0", "end")

        text_condition = self.text_entry_condition.get("1.0", "end-1c").replace(" ", "").replace(",", " y ")
        preview_text = f"Si {text_condition} entonces:\n"
        actions = self.text_entry_action.get("1.0", "end-1c").split(",")
        preview_text += "\n".join(f"\t{action.strip()}" for action in actions)

        self.text_preview.insert("1.0", preview_text)
        self.text_preview.configure(state="disabled")

    def delete(self):
        """Elimina el frame de la interfaz."""
        self.main_container.pack_forget()
