import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATOS = os.path.join(BASE_DIR, "datos")


class ArchivoServicio:
    def __init__(self, ruta_datos=RUTA_DATOS):
        self.ruta_datos = ruta_datos
        os.makedirs(self.ruta_datos, exist_ok=True)

    def _ruta_archivo(self, nombre_archivo):
        return os.path.join(self.ruta_datos, nombre_archivo)

    def leer_json(self, nombre_archivo, valor_defecto=None):
        ruta = self._ruta_archivo(nombre_archivo)
        if not os.path.exists(ruta):
            return valor_defecto if valor_defecto is not None else []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return valor_defecto if valor_defecto is not None else []

    def escribir_json(self, nombre_archivo, datos):
        ruta = self._ruta_archivo(nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
