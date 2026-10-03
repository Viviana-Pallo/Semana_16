class Producto:
    def __init__(self, identificador, nombre, precio, stock):
        self.identificador = identificador
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @staticmethod
    def validar_texto(valor, campo):
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")
        return valor.strip()

    @staticmethod
    def validar_numero(valor, campo):
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"El campo {campo} debe ser un numero valido.")
        if numero < 0:
            raise ValueError(f"El campo {campo} no puede ser negativo.")
        return numero

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = self.validar_numero(valor, "precio")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        self._stock = self.validar_numero(valor, "stock")
