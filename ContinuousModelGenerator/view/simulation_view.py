import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GUI_Simulation(ctk.CTkToplevel):

    def __init__(self,parent, controller):
        super().__init__(parent)
        self.entries_args = {} 
        self.controller = controller
        self.title("Simulación")
        self.geometry("1200x650")
        self.resizable(False, False)

        # === PANEL DE CONTROLES IZQUIERDO ===
        self.control_frame = ctk.CTkFrame(self, width=250, corner_radius=15)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.control_frame, text="Tiempo inicial:", width=130).pack(pady=(20, 5))
        self.tiempo_inicio = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 0.0",width=120)
        self.tiempo_inicio.pack(pady=5)

        ctk.CTkLabel(self.control_frame, text="Tiempo final:").pack(pady=(10, 5))
        self.tiempo_fin = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 10.0",width=120)
        self.tiempo_fin.pack(pady=5)

        ctk.CTkLabel(self.control_frame, text="Δt / Tolerancia:").pack(pady=(10, 5))
        self.dt_tol = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 0.01",width=120)
        self.dt_tol.pack(pady=5)

        self.toggle_menu_btn = ctk.CTkButton(self.control_frame, text="Parámetros", command=self.toggle_menu, width=120)
        self.toggle_menu_btn.pack(pady=30)

        self.toggle_menu_btn = ctk.CTkButton(self.control_frame, text="Simular", command=self.controller.execute, width=120)
        self.toggle_menu_btn.pack(pady=30)

        # === ÁREA CENTRAL PARA RESULTADOS ===
        self.resultados_frame = ctk.CTkFrame(self, corner_radius=15)
        self.resultados_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Crear un widget de pestañas
        self.tabview = ctk.CTkTabview(self.resultados_frame, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña para el gráfico
        self.tab_grafico = self.tabview.add("Gráfico")
        self.grafico_area = ctk.CTkFrame(self.tab_grafico, height=250, corner_radius=10)
        self.grafico_area.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(self.grafico_area, text="(Gráfico aquí)", anchor="center").pack(expand=True)

        # Pestaña para los resultados
        self.tab_resultados = self.tabview.add("Resultados")
        self.text_frame = ctk.CTkFrame(self.tab_resultados, corner_radius=10)
        self.text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(self.text_frame, wrap="word")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.textbox.insert("end", "Resultados de simulación...\n")

        self.widget_parameter_panel() 
        
    def widget_parameter_panel(self):
        self.parametros_panel = ctk.CTkFrame(self, width=250, corner_radius=15)
        self.parametros_visible = False  # Estado inicial oculto

        self.scroll = ctk.CTkScrollableFrame(self.parametros_panel, label_text="Parámetros y Condiciones Iniciales")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        params= self.controller.get_variables()+self.controller.get_parameters()


        # Ejemplo de parámetros dinámicos 
        for par in params:
            frame = ctk.CTkFrame(self.scroll)
            frame.pack(pady=5, fill="x", padx=10)

            label = ctk.CTkLabel(frame, text=f"{par}:", bg_color=frame.cget("fg_color"))
            label.pack(side="left", padx=(0, 5))

            entry = ctk.CTkEntry(frame, placeholder_text=f"{par}")
            entry.pack(side="left", fill="x", expand=True)

            self.entries_args[par] = entry

    def toggle_menu(self):
        if self.parametros_visible:
            self.parametros_panel.pack_forget()
            self.parametros_visible = False
        else:
            self.parametros_panel.pack(side="right", fill="y", padx=10, pady=10)
            self.parametros_visible = True


    def get_entries_args(self):
        """
        Devuelve un diccionario con el simbolo asociado y el CTkEntry correspondiente.
        """
        return self.entries_args
    
    def get_time_args(self):
        """
        Devuelve un diccionario con los argumentos de tiempo.
        """
        return {
            "t0": self.tiempo_inicio.get(),
            "tf": self.tiempo_fin.get(),
            "dt_tol": self.dt_tol.get()
        }
    
    def update_result_terminal(self, result):
        """
        Actualiza el área de resultados con el resultado de la simulación.
        """

        self.textbox.configure(state="normal")  # Asegúrate de poder escribir
        self.textbox.delete("1.0", "end")

        # Encabezado (primera fila)
        header = "\t".join(map(str, result[0])) + "\n"
        self.textbox.insert("end", header)
        self.textbox.insert("end", "-" * 60 + "\n")

        # Filas con formato numérico
        for row in result[1:]:
            formatted = "\t".join(f"{float(x):.4f}" for x in row)
            self.textbox.insert("end", formatted + "\n")

        self.textbox.see("end")
        self.textbox.configure(state="disabled")  # Bloquear edición

    def update_result_plot(self, result):
        """
        Actualiza el área de resultados con el resultado de la simulación.
        """
        # Encabezado
        header = result[0]  
        
        # Convertir los valores numéricos a float
        data = [[float(x.replace(',', '.')) for x in row] for row in result[1:]]  
        
        # Transponer para obtener listas de columnas
        columns = list(zip(*data))
        
        # Eje x = tiempo
        t = columns[0]

        # Crear figura
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Graficar cada variable
        for i in range(1, len(header)):
            ax.plot(t, columns[i], label=header[i])

        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valores')
        ax.legend()
        ax.grid(True)

        # Limpiar área del gráfico
        for widget in self.grafico_area.winfo_children():
            widget.destroy()

        # Mostrar gráfico
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)