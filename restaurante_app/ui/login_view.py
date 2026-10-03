import tkinter as tk
from tkinter import messagebox


class LoginView(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self.title("Sabor Andino - Inicio de sesion")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg="#2d2d2d")
        self._construir_interfaz()

    def _construir_interfaz(self):
        contenedor = tk.Frame(self, bg="#2d2d2d")
        contenedor.pack(expand=True)

        tk.Label(contenedor, text="🍽️", font=("Arial", 48), bg="#2d2d2d",
                 fg="#f0a500").pack(pady=(0, 10))
        tk.Label(contenedor, text="Sabor Andino", font=("Arial", 24, "bold"),
                 bg="#2d2d2d", fg="#ffffff").pack()
        tk.Label(contenedor, text="Sistema de gestion del restaurante",
                 font=("Arial", 11), bg="#2d2d2d", fg="#cccccc").pack(pady=(0, 25))

        marco = tk.Frame(contenedor, bg="#3d3d3d", padx=35, pady=25)
        marco.pack()

        tk.Label(marco, text="Usuario", bg="#3d3d3d", fg="#ffffff",
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.entrada_usuario = tk.Entry(marco, font=("Arial", 11), width=25)
        self.entrada_usuario.grid(row=1, column=0, pady=(4, 12))

        tk.Label(marco, text="Contrasena", bg="#3d3d3d", fg="#ffffff",
                 font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.entrada_contrasena = tk.Entry(marco, font=("Arial", 11), width=25, show="*")
        self.entrada_contrasena.grid(row=3, column=0, pady=(4, 18))

        boton = tk.Button(marco, text="Ingresar", font=("Arial", 11, "bold"),
                          bg="#f0a500", fg="#2d2d2d", padx=30, pady=6,
                          command=self._iniciar_sesion)
        boton.grid(row=4, column=0)

        self.entrada_usuario.bind("<Return>", lambda e: self.entrada_contrasena.focus())
        self.entrada_contrasena.bind("<Return>", lambda e: self._iniciar_sesion())

        self.entrada_usuario.focus()

    def _iniciar_sesion(self):
        nombre_usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()
        if not nombre_usuario or not contrasena:
            messagebox.showerror("Inicio de sesion", "Ingrese usuario y contrasena.")
            return
        usuario = self.servicio.autenticar(nombre_usuario, contrasena)
        if usuario is None:
            messagebox.showerror("Inicio de sesion", "Credenciales incorrectas.")
            return
        self.destroy()
        from ui.main_view import MainView
        MainView(self.servicio, usuario).mainloop()
