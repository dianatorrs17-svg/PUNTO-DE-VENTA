from tkinter import *
import tkinter as tk

class Proveedor(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        lbl_titulo = tk.Label(self, text="Módulo de Proveedor", font=("Arial", 16), bg="pink")
        lbl_titulo.place(x=20, y=20)
