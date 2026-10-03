import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")


class MainView(tk.Tk):
    def __init__(self, servicio, usuario):
        super().__init__()
        self.servicio = servicio
        self.usuario = usuario
        self.title("Sabor Andino - Sistema de gestion")
        self.geometry("1000x750")
        self.minsize(900, 650)

        self.usuario_seleccionado = None

        self._configurar_estilos()
        self._crear_sidebar()
        self._crear_contenido()

        # Mostrar inicio por defecto
        self.mostrar_inicio()

    # ============ ESTILOS ============
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Sidebar.TFrame", background="#2d2d2d")
        estilo.configure("Sidebar.TButton",
                         background="#2d2d2d", foreground="white",
                         font=("Segoe UI", 11), anchor="w", padding=(15, 10))
        estilo.map("Sidebar.TButton",
                   background=[("active", "#3d3d3d")])
        estilo.configure("Titulo.TLabel",
                         font=("Segoe UI", 18, "bold"), background="white")
        estilo.configure("Campo.TLabel",
                         font=("Segoe UI", 10), background="white")

    # ============ SIDEBAR ============
    def _crear_sidebar(self):
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_img = self._cargar_imagen("logo.png", (60, 60))
        if logo_img:
            logo_label = tk.Label(self.sidebar, image=logo_img,
                                  bg="#2d2d2d")
            logo_label.image = logo_img
            logo_label.pack(pady=(20, 5))
        else:
            tk.Label(self.sidebar, text="🍽️", font=("Segoe UI", 30),
                     bg="#2d2d2d", fg="#f0a500").pack(pady=(20, 5))

        tk.Label(self.sidebar, text="Sabor Andino", font=("Segoe UI", 14, "bold"),
                 bg="#2d2d2d", fg="#f0a500").pack()
        tk.Label(self.sidebar, text=f"Bienvenido, {self.usuario.nombre}",
                 font=("Segoe UI", 9), bg="#2d2d2d", fg="#cccccc").pack(pady=(0, 15))

        # Botones del menu
        self._boton_menu("Inicio", "home.png", self.mostrar_inicio)
        if self.usuario.rol == "Administrador":
            self._boton_menu("Usuarios", "users.png", self.mostrar_usuarios)
        self._boton_menu("Productos", "products.png", self.mostrar_productos)
        self._boton_menu("Ventas", "sales.png", self.mostrar_ventas)

        # Salir al final
        self._boton_menu("Salir", "logout.png", self.salir)

    def _boton_menu(self, texto, icono, comando):
        img = self._cargar_imagen(f"icons/{icono}", (24, 24))
        btn = ttk.Button(self.sidebar, text=f"  {texto}",
                         style="Sidebar.TButton", command=comando)
        if img:
            btn.config(image=img, compound="left")
            btn.image = img
        btn.pack(fill="x", padx=10, pady=2)

    def _cargar_imagen(self, ruta, tamano):
        try:
            img = Image.open(os.path.join(ASSETS, ruta))
            img = img.resize(tamano, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    # ============ CONTENIDO ============
    def _crear_contenido(self):
        self.contenido = ttk.Frame(self, style="TFrame")
        self.contenido.pack(side="left", fill="both", expand=True)

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ============ VISTA INICIO ============
    def mostrar_inicio(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Panel principal",
                  style="Titulo.TLabel").pack(pady=(30, 10))
        ttk.Label(self.contenido,
                  text=f"Bienvenido al sistema de gestion de Sabor Andino",
                  style="Campo.TLabel").pack()
        ttk.Label(self.contenido,
                  text=f"Rol: {self.usuario.rol}",
                  style="Campo.TLabel").pack(pady=(5, 0))

    # ============ VISTA USUARIOS ============
    def mostrar_usuarios(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Gestion de usuarios",
                  style="Titulo.TLabel").pack(pady=(20, 10))

        # ---- Formulario ----
        form = ttk.LabelFrame(self.contenido, text="Datos del usuario")
        form.pack(fill="x", padx=20, pady=5)

        self.identificador_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.rol_var = tk.StringVar(value="Cliente")

        self._campo(form, "Identificador:", self.identificador_var, 0)
        self._campo(form, "Nombre:", self.nombre_var, 1)
        self._campo(form, "Usuario:", self.usuario_var, 2)
        self._campo(form, "Contrasena:", self.contrasena_var, 3, mostrar="*")

        # Combobox de rol
        ttk.Label(form, text="Rol:", style="Campo.TLabel").grid(
            row=4, column=0, sticky="e", padx=5, pady=5)
        self.rol_combo = ttk.Combobox(form, textvariable=self.rol_var,
                                      values=["Empleado", "Cliente"],
                                      state="readonly", width=30)
        self.rol_combo.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Etiqueta que responde al cambio de rol (<<ComboboxSelected>>)
        self.rol_seleccionado_label = ttk.Label(
            form, text=f"Rol seleccionado: {self.rol_var.get()}",
            style="Campo.TLabel")
        self.rol_seleccionado_label.grid(row=5, column=0, columnspan=2,
                                         pady=(0, 10))

        # ---- Botones de accion ----
        acciones = ttk.Frame(self.contenido)
        acciones.pack(pady=10)
        ttk.Button(acciones, text="Registrar",
                   command=self.registrar_usuario).pack(side="left", padx=5)
        ttk.Button(acciones, text="Actualizar",
                   command=self.actualizar_usuario).pack(side="left", padx=5)
        ttk.Button(acciones, text="Eliminar",
                   command=self.eliminar_usuario).pack(side="left", padx=5)
        ttk.Button(acciones, text="Limpiar",
                   command=self.limpiar_formulario).pack(side="left", padx=5)

        # ---- Tabla de usuarios ----
        tabla_frame = ttk.Frame(self.contenido)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("identificador", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(tabla_frame, columns=columnas,
                                           show="headings", height=12)
        self.tabla_usuarios.heading("identificador", text="Identificador")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("rol", text="Rol")
        self.tabla_usuarios.column("identificador", width=120)
        self.tabla_usuarios.column("nombre", width=200)
        self.tabla_usuarios.column("usuario", width=120)
        self.tabla_usuarios.column("rol", width=120)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical",
                               command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scroll.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # ===== EVENTOS DE LA SEMANA 16 =====
        # <<TreeviewSelect>> -> cargar datos al seleccionar fila
        self.tabla_usuarios.bind("<<TreeviewSelect>>",
                                 self.al_seleccionar_usuario)
        # <Return> -> reutiliza registrar_usuario
        self.rol_combo.bind("<Return>", self.al_presionar_enter)
        # <Escape> -> limpia el formulario
        self.rol_combo.bind("<Escape>", self.al_presionar_escape)
        # <<ComboboxSelected>> -> actualiza la etiqueta de rol
        self.rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)

        self.recargar_tabla()

    def _campo(self, padre, texto, variable, fila, mostrar=None):
        ttk.Label(padre, text=texto, style="Campo.TLabel").grid(
            row=fila, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(padre, textvariable=variable, width=32,
                  show=mostrar).grid(row=fila, column=1, sticky="w", padx=5)

    # ============ CALLBACKS DE EVENTOS ============
    def al_seleccionar_usuario(self, event):
        """<<TreeviewSelect>>: carga los datos de la fila seleccionada."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        identificador = self.tabla_usuarios.item(seleccion[0], "values")[0]
        usuario = self.servicio.buscar_usuario(identificador)
        if usuario:
            self.usuario_seleccionado = usuario
            self.identificador_var.set(usuario.identificador)
            self.nombre_var.set(usuario.nombre)
            self.usuario_var.set(usuario.usuario)
            self.contrasena_var.set(usuario.contrasena)
            self.rol_var.set(usuario.rol)
            self.rol_seleccionado_label.config(
                text=f"Rol seleccionado: {usuario.rol}")

    def al_presionar_enter(self, event):
        """<Return>: reutiliza el metodo registrar_usuario."""
        self.registrar_usuario()

    def al_presionar_escape(self, event):
        """<Escape>: limpia el formulario."""
        self.limpiar_formulario()

    def al_seleccionar_rol(self, event):
        """<<ComboboxSelected>>: actualiza la etiqueta de rol."""
        self.rol_seleccionado_label.config(
            text=f"Rol seleccionado: {self.rol_var.get()}")

    # ============ OPERACIONES CRUD ============
    def registrar_usuario(self):
        identificador = self.identificador_var.get().strip()
        nombre = self.nombre_var.get().strip()
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()
        rol = self.rol_var.get()

        if not (identificador and nombre and usuario and contrasena):
            messagebox.showwarning("Campos vacios",
                                   "Complete todos los campos.")
            return

        try:
            self.servicio.registrar_usuario(
                identificador, nombre, usuario, contrasena, rol)
            messagebox.showinfo("Exito", "Usuario registrado.")
            self.limpiar_formulario()
            self.recargar_tabla()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_usuario(self):
        if not self.usuario_seleccionado:
            messagebox.showwarning("Sin seleccion",
                                   "Seleccione un usuario para actualizar.")
            return

        identificador = self.identificador_var.get().strip()
        nombre = self.nombre_var.get().strip()
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()
        rol = self.rol_var.get()

        if not (identificador and nombre and usuario and contrasena):
            messagebox.showwarning("Campos vacios",
                                   "Complete todos los campos.")
            return

        # No permitir cambiar el rol del admin autenticado
        if (self.usuario_seleccionado.identificador == self.usuario.identificador
                and rol != "Administrador"):
            messagebox.showerror("Prohibido",
                                 "No puede cambiar el rol del administrador autenticado.")
            return

        try:
            self.servicio.actualizar_usuario(
                self.usuario_seleccionado.identificador,
                nombre, usuario, contrasena, rol)
            messagebox.showinfo("Exito", "Usuario actualizado.")
            self.usuario_seleccionado = None
            self.limpiar_formulario()
            self.recargar_tabla()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        if not self.usuario_seleccionado:
            messagebox.showwarning("Sin seleccion",
                                   "Seleccione un usuario para eliminar.")
            return

        # No permitir eliminar al admin autenticado
        if self.usuario_seleccionado.identificador == self.usuario.identificador:
            messagebox.showerror("Prohibido",
                                 "No puede eliminar al administrador autenticado.")
            return

        if messagebox.askyesno("Confirmar",
                               "¿Seguro que desea eliminar este usuario?"):
            self.servicio.eliminar_usuario(
                self.usuario_seleccionado.identificador)
            self.usuario_seleccionado = None
            self.limpiar_formulario()
            self.recargar_tabla()

    def limpiar_formulario(self):
        self.identificador_var.set("")
        self.nombre_var.set("")
        self.usuario_var.set("")
        self.contrasena_var.set("")
        self.rol_var.set("Cliente")
        self.rol_seleccionado_label.config(
            text=f"Rol seleccionado: {self.rol_var.get()}")
        self.usuario_seleccionado = None
        if hasattr(self, "tabla_usuarios"):
            self.tabla_usuarios.selection_remove(
                self.tabla_usuarios.selection())

    def recargar_tabla(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        ruta = os.path.join(BASE, "datos", "usuarios.json")
        with open(ruta, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
        for u in usuarios:
            self.tabla_usuarios.insert("", "end", values=(
                u["identificador"], u["nombre"], u["usuario"], u["rol"]))

    # ============ VISTAS PRODUCTOS / VENTAS ============
    def mostrar_productos(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Gestion de productos",
                  style="Titulo.TLabel").pack(pady=(30, 10))
        ttk.Label(self.contenido, text="Seccion en construccion.",
                  style="Campo.TLabel").pack()

    def mostrar_ventas(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Registro de ventas",
                  style="Titulo.TLabel").pack(pady=(20, 10))

        # ---- Formulario ----
        form = ttk.LabelFrame(self.contenido, text="Datos de la venta")
        form.pack(fill="x", padx=20, pady=5)

        self.producto_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        ttk.Label(form, text="Producto:", style="Campo.TLabel").grid(
            row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.producto_var, width=32).grid(
            row=0, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Cantidad:", style="Campo.TLabel").grid(
            row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.cantidad_var, width=32).grid(
            row=1, column=1, sticky="w", padx=5)

        ttk.Label(form, text="Precio unitario:", style="Campo.TLabel").grid(
            row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.precio_var, width=32).grid(
            row=2, column=1, sticky="w", padx=5)

        # Etiqueta del total
        self.total_label = ttk.Label(
            form, text="Total: $0.00", style="Campo.TLabel")
        self.total_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        # ---- Botones ----
        acciones = ttk.Frame(self.contenido)
        acciones.pack(pady=10)
        ttk.Button(acciones, text="Registrar venta",
                   command=self.registrar_venta).pack(side="left", padx=5)
        ttk.Button(acciones, text="Limpiar",
                   command=self.limpiar_venta).pack(side="left", padx=5)

        # ---- Tabla de ventas ----
        tabla_frame = ttk.Frame(self.contenido)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("id", "fecha", "producto", "cantidad", "precio", "total")
        self.tabla_ventas = ttk.Treeview(tabla_frame, columns=columnas,
                                         show="headings", height=12)
        self.tabla_ventas.heading("id", text="ID")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("cantidad", text="Cantidad")
        self.tabla_ventas.heading("precio", text="Precio")
        self.tabla_ventas.heading("total", text="Total")
        self.tabla_ventas.column("id", width=50)
        self.tabla_ventas.column("fecha", width=100)
        self.tabla_ventas.column("producto", width=150)
        self.tabla_ventas.column("cantidad", width=80)
        self.tabla_ventas.column("precio", width=80)
        self.tabla_ventas.column("total", width=80)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical",
                               command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scroll.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.recargar_ventas()

    def registrar_venta(self):
        producto = self.producto_var.get().strip()
        cantidad = self.cantidad_var.get().strip()
        precio = self.precio_var.get().strip()

        if not (producto and cantidad and precio):
            messagebox.showwarning("Campos vacios",
                                   "Complete todos los campos.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error",
                                 "Cantidad debe ser entero y precio un numero.")
            return

        total = cantidad * precio

        ruta = os.path.join(BASE, "datos", "ventas.json")
        with open(ruta, "r", encoding="utf-8") as archivo:
            ventas = json.load(archivo)

        nuevo_id = (ventas[-1]["id"] + 1) if ventas else 1
        from datetime import date
        venta = {
            "id": nuevo_id,
            "fecha": date.today().isoformat(),
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "total": total,
            "usuario": self.usuario.usuario
        }
        ventas.append(venta)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(ventas, archivo, ensure_ascii=False, indent=4)

        messagebox.showinfo("Exito", f"Venta registrada. Total: ${total:.2f}")
        self.limpiar_venta()
        self.recargar_ventas()

    def limpiar_venta(self):
        self.producto_var.set("")
        self.cantidad_var.set("")
        self.precio_var.set("")
        self.total_label.config(text="Total: $0.00")

    def recargar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        ruta = os.path.join(BASE, "datos", "ventas.json")
        with open(ruta, "r", encoding="utf-8") as archivo:
            ventas = json.load(archivo)
        for v in ventas:
            self.tabla_ventas.insert("", "end", values=(
                v["id"], v["fecha"], v["producto"],
                v["cantidad"], v["precio_unitario"], v["total"]))

    # ============ SALIR ============
    def salir(self):
        self.destroy()
        from ui.login_view import LoginView
        LoginView(self.servicio).mainloop()
