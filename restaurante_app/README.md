# 🍽️ Restaurante App — Sistema de Gestión

Aplicación de escritorio desarrollada en **Python con Tkinter** para la asignatura
**Programación Orientada a Objetos (POO)**. El proyecto evoluciona semana a semana
conservando una arquitectura modular, persistencia en archivos JSON y una interfaz
gráfica clara y estilizada.

---

## 📌 Semana 16 — Manejo de eventos en Tkinter

### Propósito

El objetivo de esta semana es aplicar de forma práctica el **manejo de eventos**
dentro de una situación real del sistema: la **gestión de usuarios**. La sección de
usuarios se evoluciona para permitir **registrar, consultar, actualizar y eliminar**
usuarios mediante una tabla `Treeview` y un formulario, utilizando eventos de teclado,
eventos virtuales de `ttk` y callbacks.

### Evolución sobre la Semana 15

- Se conserva el inicio de sesión, la navegación, la gestión de productos y ventas.
- Se incorpora el atributo **`rol`** al modelo `Usuario`:
  - **Administrador**: único rol con acceso a la gestión de usuarios.
  - **Empleado** y **Cliente**: gestionables por el administrador.
- Solo el usuario con rol **Administrador** accede a la sección Usuarios.
- La contraseña **nunca** se muestra en la tabla `Treeview`.

---

## 🧱 Estructura del proyecto

restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/                  (obligatorio: íconos, logo/logotipo y recursos visuales)
├── main.py
└── README.md

### Separación de responsabilidades

| Capa        | Responsabilidad                                             |
|-------------|-------------------------------------------------------------|
| `modelos/`  | Representan los datos (Usuario, Producto, Venta) con validaciones. |
| `servicios/`| Lógica de negocio, reglas y persistencia en archivos JSON.  |
| `ui/`       | Interfaz gráfica, captura de eventos y coordinación.        |
| `main.py`   | Punto de entrada de la aplicación.                          |

---

## 👥 Gestión de usuarios

### Roles

| Rol          | Acceso a Usuarios |
|--------------|-------------------|
| Administrador| ✅ Sí             |
| Empleado     | ❌ No             |
| Cliente      | ❌ No             |

### Operaciones CRUD

- **Registrar**: crea un usuario Empleado o Cliente y lo persiste en `usuarios.json`.
- **Consultar**: al seleccionar una fila del `Treeview`, los datos se cargan en el formulario.
- **Actualizar**: modifica los datos del usuario seleccionado.
- **Eliminar**: elimina un usuario con **confirmación previa**.

### Reglas de negocio

- No se pueden registrar nuevos **Administradores** desde la pantalla.
- No se puede **eliminar** ni **cambiar el rol** del administrador autenticado.
- No se permiten **identificadores** ni **nombres de usuario** duplicados.
- La contraseña **no se muestra** en la tabla.

---

## ⚡ Manejo de eventos implementado

### 1. `<<TreeviewSelect>>` — selección de fila

```python
self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
