from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Optional

@dataclass
class Producto:
    """
    Representa la estructura de un producto según la tabla PRODUCTO de la base de datos.
    """
    codigo: str
    descripcion: str
    precio: Decimal
    existencias: int
    unidad_fk: int
    estatus: int = 1
    imagen_producto_ruta: Optional[str] = None

    def to_dict(self):
        """
        Convierte el objeto en un diccionario. 
        Útil para responder con JSON en Flask.
        """
        data = asdict(self)
        # Convertimos Decimal a float para que sea serializable a JSON
        data['precio'] = float(self.precio)
        return data

    @staticmethod
    def from_dict(data):
        """
        Crea una instancia de Producto a partir de un diccionario (como el de Postman).
        """
        return Producto(
            codigo=data.get('codigo'),
            descripcion=data.get('descripcion'),
            precio=Decimal(str(data.get('precio', 0))),
            existencias=data.get('existencias', 0),
            unidad_fk=data.get('unidad_fk'),
            estatus=data.get('estatus', 1),
            imagen_producto_ruta=data.get('imagen_producto_ruta')
        )