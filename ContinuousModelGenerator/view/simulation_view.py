import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GUI_Simulation(ctk.CTkToplevel):

    def __init__(self,parent, controller):
        super().__init__(parent)
        self.widget_parameter_panel_list={}
        self.parametros_panel_list = {}  
        self.entries_args = {} 
        self.t_ini_list = {}
        self.t_fin_list = {}
        self.dt_tol_list = {}

        self.controller = controller
        self.title("Simulación")
        self.geometry("1200x650")
        self.resizable(False, False)

        self.graphic_list = []  # Lista para almacenar frames de gráficos
        self.result_list = []  # Lista para almacenar frames de resultados
        self.fig_list = []  # Lista para almacenar figuras de matplotlib

        log_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=18, height=25)
        log_frame.pack(side="bottom", anchor="s", fill="x",pady=10, padx=10)
        log_label = ctk.CTkLabel(log_frame, text="", text_color="red", anchor="w", justify="left")
        log_label.pack(side="left", anchor="w", padx=5, pady=5)

        #Mientras que la ventana tenga el foco, se actualiza el label de errores
        self.bind("<FocusIn>",lambda event: self.controller.set_log_label(log_label))

        # Crear un widget de pestañas
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_simulacion_tab("Simulación 1")
        self.add_plus_tab()
        self.sim_count = 1  # Contador de simulaciones

    
        self.monitor_tab_change()

    
    def add_plus_tab(self):
        # Añadir pestaña "+" si no existe
        if "+" not in self.tabview._tab_dict:
            self.tabview.add("+")

    def monitor_tab_change(self):
        selected = self.tabview.get()
        if selected == "+" and self.current_tab != "+":
            self.sim_count += 1
            new_tab_name = f"Simulación {self.sim_count}"
            self.add_simulacion_tab(new_tab_name)
            self.tabview.set(new_tab_name)
        self.current_tab = selected
        self.after(100, self.monitor_tab_change)

    def on_add_tab_click(self, event=None):
        # Cada vez que se pulsa el tab de "+"
        self.sim_count += 1
        nombre_sim = f"Simulación {self.sim_count}"
        self.add_simulacion_tab(nombre_sim)
        self.tabview.set(nombre_sim)  # Cambiar a la nueva pestaña


    def add_simulacion_tab(self, name_tab):
        # Eliminar "+" temporalmente
        if "+" in self.tabview._tab_dict:
            self.tabview.delete("+")
        
        self.entries_args[name_tab] = {}  # Diccionario para almacenar entradas de parámetros
        self.t_ini_list[name_tab] = {}
        self.t_fin_list[name_tab] = {}
        self.dt_tol_list[name_tab] = {}

        # Crear pestaña para esta simulación
        self.tabview.add(name_tab)
        inner_tab =  self.tabview.tab(name_tab)

         # === PANEL DE CONTROLES IZQUIERDO ===
        self.control_frame = ctk.CTkFrame(inner_tab, width=250, corner_radius=15)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(self.control_frame, text="Tiempo inicial:", width=130).pack(pady=(20, 5))
        self.t_ini_list[name_tab] = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 0.0",width=120)
        self.t_ini_list[name_tab].pack(pady=5)

        ctk.CTkLabel(self.control_frame, text="Tiempo final:").pack(pady=(10, 5))
        self.t_fin_list[name_tab] = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 10.0",width=120)
        self.t_fin_list[name_tab].pack(pady=5)

        text = "Tolerancia:" if self.controller.model.method == "runge-kutta-fehlberg" else "Δt"
        ctk.CTkLabel(self.control_frame, text=text).pack(pady=(10, 5))
        self.dt_tol_list[name_tab] = ctk.CTkEntry(self.control_frame, placeholder_text="Ej: 0.01",width=120)
        self.dt_tol_list[name_tab].pack(pady=5)

        self.toggle_menu_btn = ctk.CTkButton(self.control_frame, text="Simular", command=self.controller.execute, width=120)
        self.toggle_menu_btn.pack(pady=30)

        self.toggle_menu_btn = ctk.CTkButton(self.control_frame, text="Exportar PDF", command=self.controller.export_pdf, width=120)
        self.toggle_menu_btn.pack(pady=30)
       
        self.widget_parameter_panel(inner_tab, name_tab)

         # === ÁREA CENTRAL PARA RESULTADOS ===
        self.resultados_frame = ctk.CTkFrame(inner_tab, corner_radius=15)
        self.resultados_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        sim_tab = ctk.CTkTabview(self.resultados_frame, corner_radius=10)
        sim_tab.pack(fill="both", expand=True, padx=10, pady=10)


       # Pestaña para el gráfico
        tab_grafico = sim_tab.add("Gráfico")
        grafico_area = ctk.CTkFrame(tab_grafico, height=250, corner_radius=10)
        grafico_area.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(grafico_area, text="(Gráfico aquí)", anchor="center").pack(expand=True)
        self.graphic_list.append(grafico_area)  # Guardar referencia para actualizar el gráfico
        
        # Pestaña para los resultados
        tab_resultados = sim_tab.add("Resultados")
        text_frame = ctk.CTkFrame(tab_resultados, corner_radius=10)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        textbox = ctk.CTkTextbox(text_frame, wrap="word")
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        textbox.insert("end", "Resultados de simulación...\n")
        self.result_list.append(textbox)  # Guardar referencia para actualizar los resultados

        self.add_plus_tab()  # Añadir de nuevo la pestaña "+" al final
         

    def widget_parameter_panel(self, frame, name_tab):
        self.widget_parameter_panel_list[name_tab] = ctk.CTkFrame(frame, width=250, corner_radius=15)
        self.widget_parameter_panel_list[name_tab].pack(side="right", fill="y", padx=10, pady=10)

        self.scroll = ctk.CTkScrollableFrame(self.widget_parameter_panel_list[name_tab], 
                                             label_text="Parámetros y Condiciones Iniciales")
        self.scroll.pack(fill="both",  expand=True, padx=10, pady=10)

        params= self.controller.get_variables()+self.controller.get_parameters()

        for par in params:
            frame = ctk.CTkFrame(self.scroll)
            frame.pack(pady=5, fill="x", padx=10)

            label = ctk.CTkLabel(frame, text=f"{par}:", bg_color=frame.cget("fg_color"))
            label.pack(side="left", padx=(0, 5))

            entry = ctk.CTkEntry(frame, placeholder_text=f"{par}")
            entry.pack(side="left", fill="x", expand=True)

            self.entries_args[name_tab][par] = entry
            print(f"Entrada añadida para {name_tab}: {par}")

    def toggle_menu(self):
        if self.widget_parameter_panel_list[self.tabview.get()]:
            self.widget_parameter_panel_list[self.tabview.get()].pack_forget()
            self.parametros_panel_list[self.tabview.get()] = False
        else:
            
            self.parametros_visible_list[self.tabview.get()] = True


    def get_entries_args(self):
        """
        Devuelve un diccionario con el simbolo asociado y el CTkEntry correspondiente.
        """

        print(f"Entradas args: {self.tabview.get()}")
        return self.entries_args[self.tabview.get()]
    
    def get_time_args(self):
        """
        Devuelve un diccionario con los argumentos de tiempo.
        """
        return {
            "t0": self.t_ini_list[self.tabview.get()].get(),
            "tf": self.t_fin_list[self.tabview.get()].get(),
            "dt_tol": self.dt_tol_list[self.tabview.get()].get()
        }
    
    def get_result_text(self):
        """
        Obtiene el contenido visible del área de texto de resultados.
        """
        index_tab = self.tabview.get()
        textbox = self.result_list[self.tabview.index(index_tab)]

        textbox.configure(state="normal")
        content = textbox.get("1.0", "end-1c")  # Obtener texto sin salto final
        textbox.configure(state="disabled")

        return content

    def get_result_figure(self):
        """
        Obtiene el objeto Figure que está siendo mostrado en el área de gráficos.
        """
        index_tab = self.tabview.get()
        fig = self.fig_list[self.tabview.index(index_tab)]
    
        return fig
    
    
    def update_result_terminal(self, result):
        """
        Actualiza el área de resultados con el resultado de la simulación.
        """
        # Obtenemos el índice de la pestaña actual
        index_tab = self.tabview.get()
        # Obtenemos el textbox correspondiente a la pestaña actual
        textbox = self.result_list[self.tabview.index(index_tab)]

        textbox.configure(state="normal")  # Asegúrate de poder escribir
        textbox.delete("1.0", "end")

        # Encabezado (primera fila)
        header = "\t".join(map(str, result[0])) + "\n"
        textbox.insert("end", header)
        textbox.insert("end", "-" * 60 + "\n")

        # Filas con formato numérico
        for row in result[1:]:
            formatted = "\t".join(f"{float(x):.4f}" for x in row)
            textbox.insert("end", formatted + "\n")

        textbox.see("end")
        textbox.configure(state="disabled")  # Bloquear edición

   

    def update_result_plot(self, result):
        """
        Actualiza el área de resultados con el resultado de la simulación.
        """
        # Obtenemos el índice de la pestaña actual
        index_tab = self.tabview.get()
        # Obtenemos el área de gráfico correspondiente a la pestaña actual
        grafico_area = self.graphic_list[self.tabview.index(index_tab)]

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

        # Configurar gráfico
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valores')
        ax.legend()
        ax.grid(True)

        # Limpiar área del gráfico
        for widget in grafico_area.winfo_children():
            widget.destroy()

        #Comprobamos si el indice de la lista de figuras es menor que el índice de la pestaña actual
        if len(self.fig_list) <= self.tabview.index(index_tab):
            self.fig_list.append(fig)
        else:
            self.fig_list[self.tabview.index(index_tab)] = fig
        
        # Mostrar gráfico
        canvas = FigureCanvasTkAgg(fig, master=grafico_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)