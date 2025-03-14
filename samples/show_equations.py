import sympy as sp
import tkinter as tk
from tkinter import ttk  # Para el Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Definir símbolos comunes
t = sp.Symbol('t')  # Variable de tiempo
T = sp.Function('T')(t)  # Función dependiente del tiempo
m, k, c, P = sp.symbols('m k c P')  # Constantes

# Definir ecuaciones diferenciales
ecuaciones = {
    "Sistema de calefacción": sp.Eq(T.diff(t) + k * T, P),
    "Oscilador armónico": sp.Eq(m * T.diff(t, t) + c * T.diff(t) + k * T, 0),
    "Crecimiento poblacional": sp.Eq(T.diff(t), k * T * (1 - T / P))
}

def mostrar_expresion():
    """Muestra la ecuación seleccionada en la interfaz"""
    ecuacion_seleccionada = combo.get()  # Obtener la ecuación seleccionada
    if ecuacion_seleccionada in ecuaciones:
        eq = ecuaciones[ecuacion_seleccionada]
        latex_expr = sp.latex(eq)  # Convertir la ecuación a LaTeX

        # Crear la figura con matplotlib
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.text(0.5, 0.5, f"${latex_expr}$", fontsize=15, ha='center', va='center')
        ax.axis('off')

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        canvas.draw()

# Crear ventana de Tkinter
root = tk.Tk()
root.title("Selector de Ecuación Diferencial")

# Lista desplegable (Combobox)
combo = ttk.Combobox(root, values=list(ecuaciones.keys()), state="readonly")
combo.pack()
combo.current(0)  # Seleccionar la primera ecuación por defecto

# Botón para mostrar la ecuación
btn_mostrar = tk.Button(root, text="Mostrar Ecuación", command=mostrar_expresion)
btn_mostrar.pack()

root.mainloop()