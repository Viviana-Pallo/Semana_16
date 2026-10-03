from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self):
        self.archivo_servicio = ArchivoServicio()
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        self.cargar_usuarios()
        self.cargar_productos()
        self.cargar_ventas()

    def cargar_usuarios(self):
        datos = self.archivo_servicio.leer_json("usuarios.json", [])
        self.usuarios = []
        for item in datos:
            try:
                usuario = Usuario(
                    item.get("identificador", ""),
                    item.get("nombre", ""),
                    item.get("usuario", ""),
                    item.get("contrasena", ""),
                    item.get("rol", "Cliente"),
                )
                self.usuarios.append(usuario)
            except ValueError:
                continue

    def cargar_productos(self):
        datos = self.archivo_servicio.leer_json("productos.json", [])
        self.productos = []
        for item in datos:
            try:
                producto = Producto(
                    item.get("identificador", ""),
                    item.get("nombre", ""),
                    item.get("precio", 0),
                    item.get("stock", 0),
                )
                self.productos.append(producto)
            except ValueError:
                continue

    def cargar_ventas(self):
        datos = self.archivo_servicio.leer_json("ventas.json", [])
        self.ventas = []
        for item in datos:
            try:
                venta = Venta(
                    item.get("identificador", ""),
                    item.get("producto", ""),
                    item.get("cantidad", 0),
                    item.get("total", 0),
                    item.get("fecha", ""),
                )
                self.ventas.append(venta)
            except ValueError:
                continue

    # ===== Autenticacion =====
    def autenticar(self, nombre_usuario, contrasena):
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario and usuario.contrasena == contrasena:
                return usuario
        return None

    # ===== Usuarios =====
    def listar_usuarios(self):
        return list(self.usuarios)

    def buscar_usuario_por_identificador(self, identificador):
        identificador = identificador.strip()
        for usuario in self.usuarios:
            if usuario.identificador == identificador:
                return usuario
        return None

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        nombre_usuario = nombre_usuario.strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    def guardar_usuarios(self):
        datos = [
            {
                "identificador": usuario.identificador,
                "nombre": usuario.nombre,
                "usuario": usuario.usuario,
                "contrasena": usuario.contrasena,
                "rol": usuario.rol,
            }
            for usuario in self.usuarios
        ]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def registrar_usuario(self, identificador, nombre, usuario, contrasena, rol):
        nuevo_usuario = Usuario(identificador, nombre, usuario, contrasena, rol)
        if nuevo_usuario.rol == "Administrador":
            raise ValueError("No se pueden registrar nuevos administradores desde esta pantalla.")
        if self.buscar_usuario_por_identificador(nuevo_usuario.identificador) is not None:
            raise ValueError("Ya existe un usuario con ese identificador.")
        if self.buscar_usuario_por_nombre_usuario(nuevo_usuario.usuario) is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(self, identificador, nombre, usuario, contrasena, rol,
                           identificador_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")
        datos_validados = Usuario(identificador, nombre, usuario, contrasena, rol)
        usuario_con_mismo_login = self.buscar_usuario_por_nombre_usuario(datos_validados.usuario)
        if (usuario_con_mismo_login is not None
                and usuario_con_mismo_login.identificador != usuario_actual.identificador):
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")
        if (identificador_usuario_actual == usuario_actual.identificador
                and usuario_actual.rol == "Administrador"
                and datos_validados.rol != "Administrador"):
            raise ValueError("No puede cambiar el rol del administrador actual.")
        usuario_actual.nombre = datos_validados.nombre
        usuario_actual.usuario = datos_validados.usuario
        usuario_actual.contrasena = datos_validados.contrasena
        usuario_actual.rol = datos_validados.rol
        self.guardar_usuarios()
        return usuario_actual

    def eliminar_usuario(self, identificador, identificador_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")
        if usuario_actual.identificador == identificador_usuario_actual:
            raise ValueError("No puede eliminar el usuario actualmente autenticado.")
        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual

    # ===== Productos =====
    def listar_productos(self):
        return list(self.productos)

    def guardar_productos(self):
        datos = [
            {
                "identificador": producto.identificador,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "stock": producto.stock,
            }
            for producto in self.productos
        ]
        self.archivo_servicio.escribir_json("productos.json", datos)

    # ===== Ventas =====
    def listar_ventas(self):
        return list(self.ventas)

    def guardar_ventas(self):
        datos = [
            {
                "identificador": venta.identificador,
                "producto": venta.producto,
                "cantidad": venta.cantidad,
                "total": venta.total,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)
