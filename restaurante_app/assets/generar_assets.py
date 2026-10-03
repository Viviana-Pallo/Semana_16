import os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
ICONS = os.path.join(ASSETS, "icons")
os.makedirs(ICONS, exist_ok=True)

AMARILLO = "#f0a500"
VERDE = "#28a745"
ROJO = "#d9534f"
GRIS = "#6c757d"


def crear_icono(nombre, color, simbolo):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 60, 60], radius=12, fill=color)
    d.text((32, 32), simbolo, fill="white", anchor="mm", font_size=28)
    img.save(os.path.join(ICONS, nombre))
    print("OK:", nombre)


# ===== Logo del restaurante (plato) =====
logo = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
d = ImageDraw.Draw(logo)
d.ellipse([10, 10, 110, 110], fill=AMARILLO)
d.ellipse([34, 34, 86, 86], fill="#2d2d2d")
d.text((60, 60), "🍽️", fill="white", anchor="mm", font_size=44)
logo.save(os.path.join(ASSETS, "logo.png"))
print("OK: logo.png")

# ===== Iconos del menu lateral =====
crear_icono("home.png", AMARILLO, "🏠")
crear_icono("users.png", AMARILLO, "👥")
crear_icono("products.png", AMARILLO, "📦")
crear_icono("sales.png", AMARILLO, "💰")
crear_icono("logout.png", ROJO, "🚪")

# ===== Iconos de acciones =====
crear_icono("add.png", VERDE, "➕")
crear_icono("edit.png", AMARILLO, "✏️")
crear_icono("delete.png", ROJO, "🗑️")
crear_icono("clean.png", GRIS, "🧹")

print("\nEstructura creada:")
print(ASSETS)
print(ICONS)
