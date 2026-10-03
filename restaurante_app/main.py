import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.login_view import LoginView
from servicios.restaurante_servicio import RestauranteServicio


def main():
    servicio = RestauranteServicio()
    app = LoginView(servicio)   # LoginView ya es la ventana Tk principal
    app.mainloop()


if __name__ == "__main__":
    main()
