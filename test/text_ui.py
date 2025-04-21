import tkinter as tk
from tkinter import messagebox

def nuevo_archivo():
    print("Nuevo archivo creado.")

def abrir_archivo():
    print("Abrir archivo.")

def salir():
    root.quit()

def mostrar_ayuda():
    messagebox.showinfo("Ayuda", "Este es un ejemplo de menú.")

root = tk.Tk()
root.title("Mi Simulador")
root.geometry("600x400")

# Crear la barra de menú
menu_bar = tk.Menu(root)

# Menú "Archivo"
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo)
menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

# Menú "Ver"
menu_ver = tk.Menu(menu_bar, tearoff=0)
menu_ver.add_checkbutton(label="Mostrar líneas de tiempo")
menu_bar.add_cascade(label="Ver", menu=menu_ver)

# Menú "Ayuda"
menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Ver Ayuda", command=mostrar_ayuda)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Asociar la barra de menú con la ventana
root.config(menu=menu_bar)

# Contenido de ejemplo
tk.Label(root, text="Bienvenido al simulador", font=("Segoe UI", 14)).pack(pady=50)

root.mainloop()
