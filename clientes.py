import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox


class Clientes(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_registros()

    def widgets(self):
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="sans 20 bold", bg="pink")
        self.labelframe.place(x=20, y=20, width=250, height=560)

        lblnombre = tk.Label(self.labelframe, text="Nombre: ", font="sans 14 bold", bg="pink")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.nombre.place(x=10, y=50, width=220, height=40)

        lblcedula = tk.Label(self.labelframe, text="Cedula: ", font="sans 14 bold", bg="pink")
        lblcedula.place(x=10, y=100)
        self.cedula = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.cedula.place(x=10, y=130, width=220, height=40)

        lbltelefono = tk.Label(self.labelframe, text="Telefono: ", font="sans 14 bold", bg="pink")
        lbltelefono.place(x=10, y=180)
        self.telefono = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.telefono.place(x=10, y=210, width=220, height=40)

        lbldireccion = tk.Label(self.labelframe, text="Direccion: ", font="sans 14 bold", bg="pink")
        lbldireccion.place(x=10, y=260)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.direccion.place(x=10, y=290, width=220, height=40)

        lblcorreo = tk.Label(self.labelframe, text="Correo: ", font="sans 14 bold", bg="pink")
        lblcorreo.place(x=10, y=340)
        self.correo = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.correo.place(x=10, y=370, width=220, height=40)

        btn1 = Button(self.labelframe, fg="black", text="Ingresar", font="sans 16 bold", command=self.registrar)
        btn1.place(x=10, y=420, width=220, height=40)

        btn2 = Button(self.labelframe, fg="black", text="Modificar", font="sans 16 bold", command=self.modificar)
        btn2.place(x=10, y=470, width=220, height=40)

        treFrame = Frame(self, bg="white")
        treFrame.place(x=280, y=20, width=800, height=560)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(
            treFrame,
            yscrollcommand=scrol_y.set,
            xscrollcommand=scrol_x.set,
            height=40,
            columns=("ID", "Nombre", "Cedula", "Telefono", "Direccion", "Correo"),
            show="headings",
        )
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        for col in ("ID", "Nombre", "Cedula", "Telefono", "Direccion", "Correo"):
            self.tre.heading(col, text=col)
            self.tre.column(col, width=150, anchor="center")

        self.tre.column("ID", width=50)

    def validar_campos(self):
        if not all([self.nombre.get(), self.cedula.get(), self.telefono.get(), self.direccion.get(), self.correo.get()]):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False
        return True

    def registrar(self):
        if not self.validar_campos():
            return

        nombre = self.nombre.get()
        cedula = self.cedula.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, cedula, telefono, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                (nombre, cedula, telefono, direccion, correo),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_treeview()
            self.limpiar_campos()
            self.cargar_registros()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def cargar_registros(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            conn.close()

            self.limpiar_treeview()
            for row in rows:
                self.tre.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")

    def limpiar_treeview(self):
        for item in self.tre.get_children():
            self.tre.delete(item)

    def limpiar_campos(self):
        for entry in [self.nombre, self.cedula, self.telefono, self.direccion, self.correo]:
            entry.delete(0, END)

    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para modificar.")
            return

        item = self.tre.selection()[0]
        id_cliente = self.tre.item(item, "values")[0]

        nombre_actual = self.tre.item(item, "values")[1]
        cedula_actual = self.tre.item(item, "values")[2]
        telefono_actual = self.tre.item(item, "values")[3]
        direccion_actual = self.tre.item(item, "values")[4]
        correo_actual = self.tre.item(item, "values")[5]

        top_modificar = Toplevel(self)
        top_modificar.title("Modificar cliente")
        top_modificar.geometry("400x400+400+50")
        top_modificar.config(bg="pink")
        top_modificar.resizable(False, False)
        top_modificar.transient(self.master)
        top_modificar.grab_set()
        top_modificar.focus_set()

        tk.Label(top_modificar, text="Nombre:", font="sans 14 bold", bg="pink").grid(row=0, column=0, padx=10, pady=5)
        nombre_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        nombre_nuevo.insert(0, nombre_actual)
        nombre_nuevo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Cedula:", font="sans 14 bold", bg="pink").grid(row=1, column=0, padx=10, pady=5)
        cedula_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        cedula_nuevo.insert(0, cedula_actual)
        cedula_nuevo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Telefono:", font="sans 14 bold", bg="pink").grid(row=2, column=0, padx=10, pady=5)
        telefono_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        telefono_nuevo.insert(0, telefono_actual)
        telefono_nuevo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Direccion:", font="sans 14 bold", bg="pink").grid(row=3, column=0, padx=10, pady=5)
        direccion_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        direccion_nuevo.insert(0, direccion_actual)
        direccion_nuevo.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Correo:", font="sans 14 bold", bg="pink").grid(row=4, column=0, padx=10, pady=5)
        correo_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        correo_nuevo.insert(0, correo_actual)
        correo_nuevo.grid(row=4, column=1, padx=10, pady=5)

        def guardar_modificaciones():
            nuevo_nombre = nombre_nuevo.get()
            nueva_cedula = cedula_nuevo.get()
            nuevo_telefono = telefono_nuevo.get()
            nueva_direccion = direccion_nuevo.get()
            nuevo_correo = correo_nuevo.get()

            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE clientes
                    SET nombre = ?, cedula = ?, telefono = ?, direccion = ?, correo = ?
                    WHERE id = ?
                    """,
                    (nuevo_nombre, nueva_cedula, nuevo_telefono, nueva_direccion, nuevo_correo, id_cliente),
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                self.limpiar_treeview()
                self.cargar_registros()
                top_modificar.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")

        btn_guardar = tk.Button(
            top_modificar,
            text="Guardar cambios",
            command=guardar_modificaciones,
            font=("sans", 14, "bold"),
        )
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)


