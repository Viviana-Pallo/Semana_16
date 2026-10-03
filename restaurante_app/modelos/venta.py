class Venta:
    def __init__(self, identificador, producto, cantidad, total, fecha):
        self.identificador = identificador
        self.producto = producto
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha

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
    def producto(self):
        return self._producto

    @producto.setter
    def producto(self, valor):
        self._producto = self.validar_texto(valor, "producto")

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        self._cantidad = self.validar_numero(valor, "cantidad")

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, valor):
        self._total = self.validar_numero(valor, "total")

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_texto(valor, "fecha")
