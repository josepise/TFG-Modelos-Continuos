import tkinter as tk
from tkinter import messagebox
import subprocess

# --- Funciones del Menú ---
def nuevo_archivo():
    terminal.insert(tk.END, "> Nuevo archivo creado.\n")
    
def abrir_archivo():
    terminal.insert(tk.END, "> Abrir archivo.\n")

def guardar_archivo():
    terminal.insert(tk.END, "> Archivo guardado.\n")

def cortar():
    terminal.insert(tk.END, "> Cortar texto.\n")

def copiar():
    terminal.insert(tk.END, "> Copiar texto.\n")

def pegar():
    terminal.insert(tk.END, "> Pegar texto.\n")

def configurar_pagina():
    terminal.insert(tk.END, "> Configurando la página.\n")

def cambiar_margen():
    terminal.insert(tk.END, "> Cambiando márgenes.\n")

# --- Función para ejecutar comandos en la terminal ---
def ejecutar_comando(event=None):
    comando = entrada.get()
    if comando.lower() == "exit":
        root.destroy()
        return

    entrada.delete(0, tk.END)
    
    try:
        salida = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        salida = e.output

    terminal.insert(tk.END, f"> {comando}\n{salida}\n")
    terminal.see(tk.END)

# --- Crear la ventana principal ---
root = tk.Tk()
root.title("Menú y Terminal en Tkinter")
root.geometry("600x400")

# --- Crear la barra de menú ---
menu_bar = tk.Menu(root)

# Menú Archivo
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo)
menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_command(label="Guardar", command=guardar_archivo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)

# Menú Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_editar.add_command(label="Cortar", command=cortar)
menu_editar.add_command(label="Copiar", command=copiar)
menu_editar.add_command(label="Pegar", command=pegar)

# Menú Diseño de Página
menu_diseno = tk.Menu(menu_bar, tearoff=0)
menu_diseno.add_command(label="Configurar página", command=configurar_pagina)
menu_diseno.add_command(label="Cambiar márgenes", command=cambiar_margen)

# Agregar los menús a la barra de menú
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
menu_bar.add_cascade(label="Diseño de Página", menu=menu_diseno)

# Asignar la barra de menú a la ventana
root.config(menu=menu_bar)

# --- Crear el área de terminal ---
terminal = tk.Text(root, bg="black", fg="white", font=("Consolas", 12))
terminal.pack(expand=True, fill="both")

# Crear la entrada de comandos
entrada = tk.Entry(root, bg="black", fg="white", font=("Consolas", 12))
entrada.pack(fill="x")
entrada.bind("<Return>", ejecutar_comando)  # Ejecutar al presionar Enter

# Ejecutar la aplicación
root.mainloop()
