import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Login(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre, bg="purple")
        self.controlador = controlador
        self.widgets()

    def validacion(self, user, pas):
        return len(user) > 0 and len(pas) > 0

    def verificar_login(self):
        user = self.entry_usuario.get()
        pas = self.entry_pass.get()

        if not self.validacion(user, pas):
            messagebox.showerror("Error", "Llene todas las casillas")
            return

        consulta = "SELECT * FROM usuarios WHERE username=? AND password=?"
        parametros = (user, pas)

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                result = cursor.fetchall()
                if result:
                    messagebox.showinfo("Bienvenido", f"Acceso correcto, {user}")

                   
                    from container import Container
                    self.controlador.show_frame(Container)

                else:
                    self.entry_usuario.delete(0, "end")
                    self.entry_pass.delete(0, "end")
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except sqlite3.Error as e:
            messagebox.showerror("Error BD", f"Ocurrió un error: {e}")

    def widgets(self):
       
        try:
            self.bg_image = Image.open("imagenes/fondopg.jpg")
            self.bg_image = self.bg_image.resize((1100, 650), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, width=1100, height=650)
        except Exception as e:
            print("Error cargando el fondo:", e)
            self.configure(bg="gray")

        
        frame_login = tk.Frame(self, bg="white", bd=2, relief="groove")
        frame_login.place(relx=0.5, rely=0.5, anchor="center", width=420, height=500)

       
        try:
            self.logo_image = Image.open("imagenes/logo.jpg")
            self.logo_image = self.logo_image.resize((120, 120), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(frame_login, image=self.logo_image, bg="white")
            self.logo_label.pack(pady=(10, 5))
        except Exception as e:
            print("Error cargando el logo:", e)

        
        lbl_titulo = tk.Label(frame_login, text="Inicio de Sesión", font=("Arial", 16, "bold"), bg="white")
        lbl_titulo.pack(pady=(8, 6))

        lbl_usuario = tk.Label(frame_login, text="Nombre de usuario", font=("Arial", 12), bg="white")
        lbl_usuario.pack(pady=(6, 2))
        self.entry_usuario = tk.Entry(frame_login, font=("Arial", 12))
        self.entry_usuario.pack(pady=4, ipadx=60, ipady=6)

      
        lbl_pass = tk.Label(frame_login, text="Contraseña", font=("Arial", 12), bg="white")
        lbl_pass.pack(pady=(8, 2))
        self.entry_pass = tk.Entry(frame_login, show="*", font=("Arial", 12))
        self.entry_pass.pack(pady=4, ipadx=60, ipady=6)

        
        btn_login = tk.Button(
            frame_login,
            text="Iniciar Sesión",
            font=("Arial", 12, "bold"),
            command=self.verificar_login,
            relief="raised"
        )
        btn_login.pack(fill="x", padx=40, pady=(10, 8), ipady=6)

       
        btn_registro = tk.Button(
            frame_login,
            text="Registrarse",
            font=("Arial", 12, "bold"),
            command=lambda: self.controlador.show_frame(Registro),
            relief="raised"
        )
        btn_registro.pack(fill="x", padx=40, pady=(0, 8), ipady=6)


class Registro(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre, bg="pink")
        self.controlador = controlador
        self.widgets()

    def registrar_usuario(self):
        user = self.entry_usuario.get()
        pas = self.entry_pass.get()

        if not user or not pas:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                    (user, pas)
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.controlador.show_frame(Login)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")
        except sqlite3.Error as e:
            messagebox.showerror("Error BD", f"Ocurrió un error: {e}")

    def widgets(self):
        frame_registro = tk.Frame(self, bg="white", bd=2, relief="groove")
        frame_registro.place(relx=0.5, rely=0.5, anchor="center", width=420, height=500)

       
        try:
            self.logo_image = Image.open("imagenes/logo.jpg")
            self.logo_image = self.logo_image.resize((120, 120), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(frame_registro, image=self.logo_image, bg="white")
            self.logo_label.pack(pady=(10, 5))
        except Exception as e:
            print("Error cargando el logo:", e)

        lbl_titulo = tk.Label(frame_registro, text="Registro de Usuario", font=("Arial", 16, "bold"), bg="white")
        lbl_titulo.pack(pady=(8, 6))

        
        lbl_usuario = tk.Label(frame_registro, text="Nuevo Usuario", font=("Arial", 12), bg="white")
        lbl_usuario.pack(pady=(6, 2))
        self.entry_usuario = tk.Entry(frame_registro, font=("Arial", 12))
        self.entry_usuario.pack(pady=4, ipadx=60, ipady=6)

        
        lbl_pass = tk.Label(frame_registro, text="Nueva Contraseña", font=("Arial", 12), bg="white")
        lbl_pass.pack(pady=(8, 2))
        self.entry_pass = tk.Entry(frame_registro, show="*", font=("Arial", 12))
        self.entry_pass.pack(pady=4, ipadx=60, ipady=6)

        
        btn_registrar = tk.Button(
            frame_registro,
            text="Registrar",
            font=("Arial", 12, "bold"),
            command=self.registrar_usuario,
            relief="raised"
        )
        btn_registrar.pack(fill="x", padx=40, pady=(8, 4), ipady=6)

        
        btn_volver = tk.Button(
            frame_registro,
            text="Volver al Login",
            font=("Arial", 12, "bold"),
            command=lambda: self.controlador.show_frame(Login),
            relief="raised"
        )
        btn_volver.pack(fill="x", padx=40, pady=(0, 8), ipady=6)
