import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
       
        self.image_path = None 
       
        self.articulo_seleccionado_id = None 
        self.widgets()
        self.cargar_articulos()
       
        self.timer_articulos = None

        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        
        default_image_path = os.path.join(self.image_folder, "default.png")
        if not os.path.exists(default_image_path):
            try:
              
                default_img = Image.new('RGB', (1, 1), color = 'white')
                default_img.save(default_image_path)
            except Exception:
                pass


        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                articulo TEXT NOT NULL,
                precio REAL,
                costo REAL,
                stock INTEGER,
                estado TEXT,
                image_path TEXT
            )
        """)
        self.con.commit()

        
        self.articulos_combobox()

    def articulos_combobox(self):
        """Carga la lista de artículos para el Combobox de búsqueda."""
        self.cur.execute("SELECT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos

    def widgets(self):
        
        canvas_articulos = tk.LabelFrame(
            self,
            text="Artículos",
            font="arial 14 bold",
            bg="pink"
        )
        canvas_articulos.place(x=300, y=10, width=780, height=580)

       
        self.canvas = tk.Canvas(canvas_articulos, bg="pink")
        self.scrollbar = tk.Scrollbar(
            canvas_articulos,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(self.canvas, bg="pink")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        
        lblframe_buscar = tk.LabelFrame(self, text="Buscar", font="arial 14 bold", bg="pink")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelect>>", self.buscar_producto)
        self.comboboxbuscar.bind("<Return>", self.buscar_producto)
        
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos_live) 

        
        lblframe_seleccion = tk.LabelFrame(self, text="Selección", font="arial 14 bold", bg="pink")
        lblframe_seleccion.place(x=10, y=95, width=280, height=170) # Altura ajustada

        
        self.label1 = tk.Label(lblframe_seleccion, text="Articulo: ", font="arial 12", bg="pink", wraplength=200, anchor="w", justify="left")
        self.label1.place(x=5, y=5, height=25)
        self.label2 = tk.Label(lblframe_seleccion, text="Precio: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label2.place(x=5, y=30, height=25)
        self.label3 = tk.Label(lblframe_seleccion, text="Costo: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label3.place(x=5, y=55, height=25)
        self.label4 = tk.Label(lblframe_seleccion, text="Stock: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label4.place(x=5, y=80, height=25)
        self.label5 = tk.Label(lblframe_seleccion, text="Estado: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label5.place(x=5, y=105, height=25)

       
        lblframe_botones = tk.LabelFrame(self, bg="pink", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=275, width=280, height=315) # Posición y altura ajustadas

        
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 16 bold", bg="#F0F0F0", fg="black",
                             command=self.agregar_articulo)
        btn1.place(x=20, y=30, width=240, height=80)

        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 16 bold", bg="#F0F0F0", fg="black")
        btn2.place(x=20, y=130, width=240, height=80)

        


    def load_image(self, frame_destino):
        """Permite al usuario seleccionar y guardar una imagen para el nuevo artículo."""
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
           
            image_to_save = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image_to_save.save(image_save_path)

           
            image_display = image.resize((200, 200), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image_display)
            self.image_path = image_save_path

            img_label = tk.Label(frame_destino, image=self.image_tk)
            img_label.image = self.image_tk # Guardar referencia para evitar que GC la borre
            img_label.place(x=0, y=0, width=200, height=200)

    
    
    def filtrar_articulos_live(self, event=None):
        """Filtra los artículos mostrados en el scrollable_frame mientras el usuario escribe."""
        filtro = self.comboboxbuscar.get()
        
        
        if self.timer_articulos is not None:
            self.after_cancel(self.timer_articulos)

        
        self.timer_articulos = self.after(300, lambda: self.cargar_articulos(filtro=filtro))


    def agregar_articulo(self):
        """Crea la ventana Toplevel para agregar un nuevo artículo."""
       
        self.image_path = None 
        
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="pink")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        tk.Label(top, text="Artículos", font="arial 12 bold", bg="pink").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Precio", font="arial 12 bold", bg="pink").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)

        tk.Label(top, text="Costo", font="arial 12 bold", bg="pink").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)

        tk.Label(top, text="Stock", font="arial 12 bold", bg="pink").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)

        tk.Label(top, text="Estado", font="arial 12 bold", bg="pink").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)

        frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg.place(x=440, y=30, width=200, height=200)

        btnimage = tk.Button(top, text="Cargar Imagen", font="arial 12 bold",
                             command=lambda: self.load_image(frameimg))
        btnimage.place(x=470, y=260, width=150, height=40)

        def guardar():
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return

            
            if self.image_path:
                image_path = self.image_path
            else:
                image_path = os.path.join(self.image_folder, "default.png")

            try:
                self.cur.execute(
                    "INSERT INTO articulos(articulo, precio, costo, stock, estado, image_path) VALUES(?,?,?,?,?,?)",
                    (articulo, precio, costo, stock, estado, image_path)
                )
                self.con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente")
                self.articulos_combobox()
                self.cargar_articulos() 
                top.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al agregar el artículo: {e}")
            finally:
                self.image_path = None 

        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)

    def cargar_articulos(self, filtro=None, categoria=None):
        """Método principal para cargar y/o filtrar los artículos en el scrollable_frame."""
        
        self.after(0, self._cargar_articulos, filtro, categoria)

    def _cargar_articulos(self, filtro=None, categoria=None):
        """Lógica interna para limpiar el frame y mostrar los artículos de la BD."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        query = "SELECT articulo, precio, image_path, estado FROM articulos"
        params = []

        if filtro:
            query += " WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')

        self.cur.execute(query, params)
        articulos = self.cur.fetchall()

        self.row = 0
        self.column = 0

        for articulo, precio, image_path, estado in articulos:
            self.mostrar_articulo(articulo, precio, image_path, estado)

    def mostrar_articulo(self, articulo, precio, image_path, estado):
        """Muestra un solo artículo en el grid."""
        article_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", borderwidth=2)
        article_frame.grid(row=self.row, column=self.column, padx=10, pady=10, sticky="nsew")
        article_frame.grid_columnconfigure(0, weight=1)

        
        if estado.lower() == "activo":
            article_frame.config(highlightbackground="#4CAF50", highlightcolor="#4CAF50", highlightthickness=2) # Verde
        elif estado.lower() == "inactivo":
            article_frame.config(highlightbackground="#F44336", highlightcolor="#F44336", highlightthickness=2) # Rojo
        else:
            article_frame.config(highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
            
      
        imagen_ref = None
        if image_path and os.path.exists(image_path):
            try:
                imagen = Image.open(image_path)
                imagen = imagen.resize((150, 150), Image.LANCZOS)
                imagen_ref = ImageTk.PhotoImage(imagen)
            except Exception:
                pass

        if not imagen_ref:
            
            image_label = tk.Label(article_frame, text="Sin Imagen", bg="#EEEEEE", width=150, height=150, font="arial 10")
        else:
            image_label = tk.Label(article_frame, image=imagen_ref, width=150, height=150)
            image_label.image = imagen_ref 

        image_label.pack(side="top", expand=True, fill="both")

        name_label = tk.Label(article_frame, text=articulo, bg="#DDDDDD", anchor="center", wraplength=150, font="arial 10 bold")
        name_label.pack(side="top", fill="x", pady=(2,0))

        precio_label = tk.Label(article_frame, text=f"Precio: $ {precio:.2f}", bg="#DDDDDD", anchor="center", wraplength=150, font="arial 9")
        precio_label.pack(side="bottom", fill="x", pady=(0,2))
        
       
        article_frame.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        image_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        name_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        precio_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))


        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1
    
    def seleccionar_articulo(self, articulo):
        """Actualiza el combobox y llama a buscar_producto al hacer clic en un artículo del grid."""
        self.comboboxbuscar.set(articulo)
        self.buscar_producto()


    
    def buscar_producto(self, event=None):
        """Busca un producto por su nombre en la BD y actualiza el panel de selección."""
        articulo = self.comboboxbuscar.get()
        if articulo.strip() == "":
            messagebox.showwarning("Aviso", "Por favor selecciona o escribe un producto para buscar.")
            return

        try:
            
            self.cur.execute("SELECT id, articulo, precio, costo, stock, estado, image_path FROM articulos WHERE articulo=?", (articulo,))
            resultado = self.cur.fetchone()

            if resultado:
                id_articulo, articulo, precio, costo, stock, estado, image_path = resultado
                self.articulo_seleccionado_id = id_articulo
                
                self.label1.config(text=f"Articulo: {articulo}")
                self.label2.config(text=f"Precio: {precio:.2f}")
                self.label3.config(text=f"Costo: {costo:.2f}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")

            
                try:
                    self.img_producto.config(image='', text="")
                    self.img_producto.image = None
                except AttributeError:
                    pass

                
                if estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.articulo_seleccionado_id = None
                messagebox.showinfo("Sin resultados", "No se encontró el producto especificado.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo buscar el producto: {e}")
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        
        self.image_path = None 
       
        self.articulo_seleccionado_id = None 
        self.widgets()
        self.cargar_articulos()
        
        self.timer_articulos = None

       
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        
        default_image_path = os.path.join(self.image_folder, "default.png")
        if not os.path.exists(default_image_path):
            try:
               
                default_img = Image.new('RGB', (1, 1), color = 'white')
                default_img.save(default_image_path)
            except Exception:
                pass


        
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                articulo TEXT NOT NULL,
                precio REAL,
                costo REAL,
                stock INTEGER,
                estado TEXT,
                image_path TEXT
            )
        """)
        self.con.commit()

        
        self.articulos_combobox()

    def articulos_combobox(self):
        """Carga la lista de artículos para el Combobox de búsqueda."""
        self.cur.execute("SELECT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos

    def widgets(self):
        
        canvas_articulos = tk.LabelFrame(
            self,
            text="Artículos",
            font="arial 14 bold",
            bg="pink"
        )
        canvas_articulos.place(x=300, y=10, width=780, height=580)

        
        self.canvas = tk.Canvas(canvas_articulos, bg="pink")
        self.scrollbar = tk.Scrollbar(
            canvas_articulos,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(self.canvas, bg="pink")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Buscar
        lblframe_buscar = tk.LabelFrame(self, text="Buscar", font="arial 14 bold", bg="pink")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelect>>", self.buscar_producto)
        self.comboboxbuscar.bind("<Return>", self.buscar_producto)
        
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos_live) 

        
        lblframe_seleccion = tk.LabelFrame(self, text="Selección", font="arial 14 bold", bg="pink")
        lblframe_seleccion.place(x=10, y=95, width=280, height=170) # Altura ajustada

        
        self.label1 = tk.Label(lblframe_seleccion, text="Articulo: ", font="arial 12", bg="pink", wraplength=200, anchor="w", justify="left")
        self.label1.place(x=5, y=5, height=25)
        self.label2 = tk.Label(lblframe_seleccion, text="Precio: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label2.place(x=5, y=30, height=25)
        self.label3 = tk.Label(lblframe_seleccion, text="Costo: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label3.place(x=5, y=55, height=25)
        self.label4 = tk.Label(lblframe_seleccion, text="Stock: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label4.place(x=5, y=80, height=25)
        self.label5 = tk.Label(lblframe_seleccion, text="Estado: ", font="arial 12", bg="pink", anchor="w", justify="left")
        self.label5.place(x=5, y=105, height=25)

        
        lblframe_botones = tk.LabelFrame(self, bg="pink", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=275, width=280, height=315) 
       
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 16 bold", bg="#F0F0F0", fg="black",
                             command=self.agregar_articulo)
        btn1.place(x=20, y=30, width=240, height=80)

        
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 16 bold", bg="#F0F0F0", fg="black",
                             command=self.editar_articulo) 
        btn2.place(x=20, y=130, width=240, height=80)


    def load_image(self, frame_destino, current_path=None):
        """Permite al usuario seleccionar y guardar una imagen para el artículo."""
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            
            image_to_save = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image_to_save.save(image_save_path)

            
            image_display = image.resize((200, 200), Image.LANCZOS)
            
            self.image_tk_popup = ImageTk.PhotoImage(image_display) 
            self.image_path = image_save_path

            
            for widget in frame_destino.winfo_children():
                widget.destroy()

            img_label = tk.Label(frame_destino, image=self.image_tk_popup)
            img_label.image = self.image_tk_popup 
            img_label.place(x=0, y=0, width=200, height=200)


    def filtrar_articulos_live(self, event=None):
        """Filtra los artículos mostrados en el scrollable_frame mientras el usuario escribe."""
        filtro = self.comboboxbuscar.get()
        
        
        if self.timer_articulos is not None:
            self.after_cancel(self.timer_articulos)

        
        self.timer_articulos = self.after(300, lambda: self.cargar_articulos(filtro=filtro))


    def agregar_articulo(self):
        """Crea la ventana Toplevel para agregar un nuevo artículo."""
        self.image_path = None 
        
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
       
        top.geometry("700x400+200+50")
        top.config(bg="pink")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        
        tk.Label(top, text="Artículos", font="arial 12 bold", bg="pink").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Precio", font="arial 12 bold", bg="pink").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)

        tk.Label(top, text="Costo", font="arial 12 bold", bg="pink").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)

        tk.Label(top, text="Stock", font="arial 12 bold", bg="pink").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)

        tk.Label(top, text="Estado", font="arial 12 bold", bg="pink").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)

       
        frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg.place(x=440, y=30, width=200, height=200)

        btnimage = tk.Button(top, text="Cargar Imagen", font="arial 12 bold",
                             command=lambda: self.load_image(frameimg))
        btnimage.place(x=470, y=260, width=150, height=40)

        
        def guardar():
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return

            
            image_path_final = self.image_path if self.image_path else os.path.join(self.image_folder, "default.png")

            try:
                self.cur.execute(
                    "INSERT INTO articulos(articulo, precio, costo, stock, estado, image_path) VALUES(?,?,?,?,?,?)",
                    (articulo, precio, costo, stock, estado, image_path_final)
                )
                self.con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente")
                self.articulos_combobox()
                self.cargar_articulos() 
                top.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al agregar el artículo: {e}")
            finally:
                self.image_path = None

        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)


    def editar_articulo(self):
        """Crea la ventana Toplevel para editar un artículo existente."""
        if not self.articulo_seleccionado_id:
            messagebox.showwarning("Aviso", "Por favor, selecciona un artículo primero.")
            return

        
        self.cur.execute("SELECT articulo, precio, costo, stock, estado, image_path FROM articulos WHERE id=?", (self.articulo_seleccionado_id,))
        datos_antiguos = self.cur.fetchone()
        
        if not datos_antiguos:
            messagebox.showerror("Error", "No se encontraron los datos del artículo para editar.")
            self.articulo_seleccionado_id = None
            return

        articulo_old, precio_old, costo_old, stock_old, estado_old, image_path_old = datos_antiguos
       
        self.image_path = image_path_old 

       
        top = tk.Toplevel(self)
        top.title(f"Editar Artículo: {articulo_old}")
        top.geometry("700x400+200+50")
        top.config(bg="pink")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        
        tk.Label(top, text="Artículos", font="arial 12 bold", bg="pink").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.insert(0, articulo_old)
        entry_articulo.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Precio", font="arial 12 bold", bg="pink").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.insert(0, str(precio_old))
        entry_precio.place(x=120, y=60, width=250, height=30)

        tk.Label(top, text="Costo", font="arial 12 bold", bg="pink").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.insert(0, str(costo_old))
        entry_costo.place(x=120, y=100, width=250, height=30)

        tk.Label(top, text="Stock", font="arial 12 bold", bg="pink").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.insert(0, str(stock_old))
        entry_stock.place(x=120, y=140, width=250, height=30)

        tk.Label(top, text="Estado", font="arial 12 bold", bg="pink").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold")
        entry_estado.insert(0, estado_old)
        entry_estado.place(x=120, y=180, width=250, height=30)

       
        frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        frameimg.place(x=440, y=30, width=200, height=200)

        
        if image_path_old and os.path.exists(image_path_old):
            try:
                img = Image.open(image_path_old)
                img = img.resize((200, 200), Image.LANCZOS)
                self.image_tk_popup = ImageTk.PhotoImage(img) 
                img_label = tk.Label(frameimg, image=self.image_tk_popup)
                img_label.image = self.image_tk_popup
                img_label.place(x=0, y=0, width=200, height=200)
            except Exception:
                tk.Label(frameimg, text="Imagen no válida", bg="#EEEEEE").place(x=0, y=0, width=200, height=200)

        btnimage = tk.Button(top, text="Cambiar Imagen", font="arial 12 bold",
                             command=lambda: self.load_image(frameimg, image_path_old))
        btnimage.place(x=470, y=260, width=150, height=40)

        
        def guardar_edicion():
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return
            
            
            image_path_final = self.image_path 

            try:
                self.cur.execute(
                    """
                    UPDATE articulos SET 
                        articulo=?, precio=?, costo=?, stock=?, estado=?, image_path=? 
                    WHERE id=?
                    """,
                    (articulo, precio, costo, stock, estado, image_path_final, self.articulo_seleccionado_id)
                )
                self.con.commit()
                messagebox.showinfo("Éxito", f"Artículo '{articulo}' actualizado correctamente.")
                
                
                self.articulos_combobox()
                self.cargar_articulos() 
                self.comboboxbuscar.set(articulo)
                self.buscar_producto() 
                top.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al actualizar el artículo: {e}")
            finally:
                self.image_path = None

        tk.Button(top, text="Guardar Cambios", font="arial 12 bold", command=guardar_edicion).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)


    def cargar_articulos(self, filtro=None, categoria=None):
        """Método principal para cargar y/o filtrar los artículos en el scrollable_frame."""
        
        self.after(0, self._cargar_articulos, filtro, categoria)

    def _cargar_articulos(self, filtro=None, categoria=None):
        """Lógica interna para limpiar el frame y mostrar los artículos de la BD."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        query = "SELECT articulo, precio, image_path, estado FROM articulos"
        params = []

        if filtro:
            query += " WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')

        self.cur.execute(query, params)
        articulos = self.cur.fetchall()

        self.row = 0
        self.column = 0

        for articulo, precio, image_path, estado in articulos:
            self.mostrar_articulo(articulo, precio, image_path, estado)

    def mostrar_articulo(self, articulo, precio, image_path, estado):
        """Muestra un solo artículo en el grid."""
        article_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", borderwidth=2)
        article_frame.grid(row=self.row, column=self.column, padx=10, pady=10, sticky="nsew")
        article_frame.grid_columnconfigure(0, weight=1)

        
        if estado.lower() == "activo":
            article_frame.config(highlightbackground="#4CAF50", highlightcolor="#4CAF50", highlightthickness=2) # Verde
        elif estado.lower() == "inactivo":
            article_frame.config(highlightbackground="#F44336", highlightcolor="#F44336", highlightthickness=2) # Rojo
        else:
            article_frame.config(highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
            
       
        imagen_ref = None
        if image_path and os.path.exists(image_path):
            try:
                imagen = Image.open(image_path)
                imagen = imagen.resize((150, 150), Image.LANCZOS)
                imagen_ref = ImageTk.PhotoImage(imagen)
            except Exception:
                pass

        if not imagen_ref:
            
            image_label = tk.Label(article_frame, text="Sin Imagen", bg="#EEEEEE", width=150, height=150, font="arial 10")
        else:
            image_label = tk.Label(article_frame, image=imagen_ref, width=150, height=150)
            image_label.image = imagen_ref 

        image_label.pack(side="top", expand=True, fill="both")

        name_label = tk.Label(article_frame, text=articulo, bg="#DDDDDD", anchor="center", wraplength=150, font="arial 10 bold")
        name_label.pack(side="top", fill="x", pady=(2,0))

        precio_label = tk.Label(article_frame, text=f"Precio: $ {precio:.2f}", bg="#DDDDDD", anchor="center", wraplength=150, font="arial 9")
        precio_label.pack(side="bottom", fill="x", pady=(0,2))
        
       
        article_frame.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        image_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        name_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))
        precio_label.bind("<Button-1>", lambda event, art=articulo: self.seleccionar_articulo(art))


        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1
    
    def seleccionar_articulo(self, articulo):
        """Actualiza el combobox y llama a buscar_producto al hacer clic en un artículo del grid."""
        self.comboboxbuscar.set(articulo)
        self.buscar_producto()


    def buscar_producto(self, event=None):
        """Busca un producto por su nombre en la BD y actualiza el panel de selección."""
        articulo = self.comboboxbuscar.get()
        if articulo.strip() == "":
           
            self.articulo_seleccionado_id = None
            self.label1.config(text="Articulo: ")
            self.label2.config(text="Precio: ")
            self.label3.config(text="Costo: ")
            self.label4.config(text="Stock: ")
            self.label5.config(text="Estado: ", fg="black")
            return

        try:
            
            self.cur.execute("SELECT id, articulo, precio, costo, stock, estado, image_path FROM articulos WHERE articulo=?", (articulo,))
            resultado = self.cur.fetchone()

            if resultado:
                id_articulo, articulo, precio, costo, stock, estado, image_path = resultado
                self.articulo_seleccionado_id = id_articulo 
                
                self.label1.config(text=f"Articulo: {articulo}")
                self.label2.config(text=f"Precio: {precio:.2f}")
                self.label3.config(text=f"Costo: {costo:.2f}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")

                
                if estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.articulo_seleccionado_id = None
                messagebox.showinfo("Sin resultados", "No se encontró el producto especificado.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo buscar el producto: {e}")