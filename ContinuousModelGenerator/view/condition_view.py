from tkinter import Button, Canvas, Text, Toplevel


class GUI_Condition(Toplevel):

    def __init__(self, parent, controller, mode="add", selected=None):
        super().__init__(parent)
        self.controler = controller
        self.mode = mode

        if mode == "add":
            self.title("Añadir condición")
        elif mode == "edit":
            self.title("Editar condición")
        
        self.geometry("1091x420")
        self.configure(bg="#92A6C0")
        # self.overrideredirect(True)  # Elimina el marco de la ventana

        canvas = Canvas(
            self,
            bg="#92A6C0",
            height=420,
            width=1091,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        #Cabecera de la ventana
        canvas.create_rectangle(
            0.0,
            0.0,
            1091.0,
            27.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_text(
            485.0,
            6.0,
            anchor="nw",
            text=self.title(),
            fill="#000000",
            font=("Inter SemiBold", 12 * -1)
        )

        canvas = Canvas(
            self,
            bg = "#92A6C0",
            height = 420,
            width = 1091,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_text(
            668.0,
            42.0,
            anchor="nw",
            text="Vista Previa",
            fill="#FFFFFF",
            font=("Inter SemiBold", 12 * -1)
        )

        canvas.create_text(
            20.0,
            42.0,
            anchor="nw",
            text="Expresiones lógicas",
            fill="#FFFFFF",
            font=("Inter SemiBold", 12 * -1)
        )

        self.text_entry_condition = Text(self)
        self.text_entry_condition.place(x=20.0, y=61.0, width=621.0, height=57.0)
        self.text_entry_condition.config(
            wrap="word",
            bd=0,  # sin borde clásico
            highlightthickness=2,  # grosor del borde
            highlightbackground="black",  # color del borde cuando no está enfocado
            highlightcolor="black"  # color del borde cuando está enfocado
        )

        canvas.create_text(
            20.0,
            127.0,
            anchor="nw",
            text="Acción",
            fill="#FFFFFF",
            font=("Inter SemiBold", 12 * -1)
        )

        self.text_entry_action = Text(self, wrap="word", bd=0, highlightthickness=2, 
                                      highlightbackground="black", highlightcolor="black" )
        self.text_entry_action.place(x=20.0, y=145.0, width=621.0, height=57.0)

        canvas.create_text(
            20.0,
            206.0,
            anchor="nw",
            text="Variables",
            fill="#FFFFFF",
            font=("Inter SemiBold", 12 * -1)
        )

        
        self.text_entry_var = Text(self, wrap="word", bd=0, highlightthickness=2,
                                   highlightbackground="black", highlightcolor="black")
        self.text_entry_var.place(x=20.0, y=222.0, width=621.0, height=40.0)

        canvas.create_text(
            20.0,
            265.0,
            anchor="nw",
            text="Constantes",
            fill="#FFFFFF",
            font=("Inter SemiBold", 12 * -1)
        )

        self.text_entry_constants = Text(self, wrap="word", bd=0, highlightthickness=2)
        self.text_entry_constants.place(x=20.0, y=282.0, width=621.0, height=40.0)
        self.text_entry_constants.configure(
            wrap="word",
            bd=0, 
            highlightthickness=2, 
            highlightbackground="black", 
            highlightcolor="black"  
        )
        
        self.text_preview = Text(self, wrap="word", bd=0, highlightthickness=2,
                                 highlightbackground="black", highlightcolor="black")
        self.text_preview.place(x=668.0, y=61.0, width=403.0, height=341.0)
        self.text_preview.config(state="disabled")   # modo de solo lectura

        if self.mode == "add":
            label = "Añadir"
            comando = lambda: self.add_condition(self.text_entry_condition.get("1.0", "end-1c"),
                                                 self.text_entry_action.get("1.0", "end-1c"),
                                                 self.text_entry_var.get("1.0", "end-1c"),
                                                 self.text_entry_constants.get("1.0", "end-1c"),
                                                 self)
        elif self.mode == "edit":
            label = "Editar"
            comando = lambda: self.edit_condition(self.text_entry_condition.get("1.0", "end-1c"),
                                                 self.text_entry_action.get("1.0", "end-1c"),
                                                 self.text_entry_var.get("1.0", "end-1c"),
                                                 self.text_entry_constants.get("1.0", "end-1c"),
                                                 self)

        save_button = Button(
            self,
            text=label,
            command=comando,
            bg="#D9D9D9",
            relief="flat"
        )
        save_button.place(x=512.0, y=360.0, width=129.0, height=42.0)

        if selected:
            self.selected=selected
            self.load_data()
            self.preview_condition()  # Cargar la vista previa al abrir la ventana de edición

        #Vinculamos la vista previa a la entrada de texto de la condición y acción
        self.text_entry_condition.bind(
            "<KeyRelease>",
            lambda event: self.preview_condition()
        )
        self.text_entry_action.bind(
            "<KeyRelease>",
            lambda event: self.preview_condition()
        )




    def add_condition(self,text_logic_exp,text_action,text_var, text_constants, window):
        self.controler.add_condition(text_logic_exp,text_action,text_var, text_constants)
        window.destroy()

    def edit_equation(self,text_logic_exp,text_action,text_var, text_constants, window):
        self.controler.edit_condition(text_logic_exp,text_action,text_var, text_constants,self.selected)
        window.destroy()

    def load_data(self):
        str_cond, str_act ,list_sym, list_const = self.controler.get_condition(self.selected)

        # Cargamos la condición lógica en el cuadro de texto
        self.text_entry_condition.delete("1.0", "end")
        self.text_entry_condition.insert("1.0", str_cond)

        # Cargamos la acción en el cuadro de texto
        self.text_entry_action.delete("1.0", "end")
        self.text_entry_action.insert("1.0", str_act)

        # Cargamos las variables en el cuadro de texto
        self.text_entry_var.delete("1.0", "end")
        self.text_entry_var.insert("1.0", list_sym)

        # Cargamos las constantes en el cuadro de texto
        self.text_entry_constants.delete("1.0", "end")
        self.text_entry_constants.insert("1.0", list_const)
        
    def preview_condition(self):
        # Limpiar el cuadro de texto de vista previa
        self.text_preview.config(state="normal")
        self.text_preview.delete("1.0", "end")

        # Creamos la cadena de texto para la vista previa
        text_condition = self.text_entry_condition.get("1.0", "end-1c").replace(" ", "").replace(",", " y ")

        preview_text = f"Si {text_condition} entonces:\n"
        actions = self.text_entry_action.get("1.0", "end-1c").split(",")
        preview_text += "\n".join(f"\t{action.strip()}" for action in actions)

        # Insertamos la cadena en el cuadro de texto de vista previa
        self.text_preview.insert("1.0", preview_text)
        self.text_preview.config(state="disabled")
   