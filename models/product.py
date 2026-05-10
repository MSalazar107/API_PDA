from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Optional
import base64

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
    imagen_producto_ruta: bytes = None

    def to_dict(self):
       
        data = asdict(self)
        
        data['precio'] = float(self.precio)
        
        if self.imagen_producto_ruta:
            data['imagen_producto_ruta'] = base64.b64encode(self.imagen_producto_ruta).decode('utf-8')
        else: 
                data['imagen_producto_ruta'] = None
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