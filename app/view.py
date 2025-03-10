import tkinter as tk
from tkinter import scrolledtext

class GeneratorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Generador de Programas de Simulación Continua")
        