import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from pedidos import Pedidos
from proveedor import Proveedor 
from informacion import Informacion 

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        
       
        self.place(x=0, y=0, width=1100, height=650)
        self.frames = {}
        self.buttons = []

        
        for i in (Ventas, Inventario, Clientes, Pedidos, Proveedor, Informacion):
            frame = i(self)
            self.frames[i] = frame

            
            frame.config(bg="pink", highlightbackground="black", highlightthickness=1)
            frame.place(x=0, y=40, width=1100, height=610)

       
        self.show_frames(Ventas)
        self.widgets()  
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()
    
    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)
    
    def pedidos(self):
        self.show_frames(Pedidos)

    def proveedor(self):
        self.show_frames(Proveedor)
    
    def informacion(self):
        self.show_frames(Informacion)

    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)

        self.btn_ventas = tk.Button(frame2, fg="black", text="Ventas", font="sans 10 bold", command=self.ventas)
        self.btn_ventas.place(x=0, y=0, width=184, height=40)

        self.btn_inventario = tk.Button(frame2, fg="black", text="Inventario", font="sans 10 bold", command=self.inventario)
        self.btn_inventario.place(x=184, y=0, width=184, height=40)
        
        self.btn_clientes = tk.Button(frame2, fg="black", text="Clientes", font="sans 10 bold", command=self.clientes)
        self.btn_clientes.place(x=369, y=0, width=184, height=40)

        self.btn_pedidos = tk.Button(frame2, fg="black", text="Pedidos", font="sans 10 bold", command=self.pedidos)
        self.btn_pedidos.place(x=554, y=0, width=184, height=40)

        self.btn_proveedor = tk.Button(frame2, fg="black", text="Proveedor", font="sans 10 bold", command=self.proveedor)
        self.btn_proveedor.place(x=739, y=0, width=184, height=40)

        self.btn_informacion = tk.Button(frame2, fg="black", text="Informacion", font="sans 10 bold", command=self.informacion)
        self.btn_informacion.place(x=923, y=0, width=184, height=40)
        
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Ventas")
    root.geometry("1100x650")

    app = Container(root, None)  
    root.mainloop()

