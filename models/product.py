from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Optional
import base64

@dataclass
class Producto:
    
    codigo: str
    descripcion: str
    precio: Decimal
    existencias: int
    unidad_fk: int
    estatus: int = 1
    imagen_producto_ruta:Optional [bytes] = None

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
        imagen = data.get('imagen_producto_ruta')
        
        if isinstance(imagen, str) and imagen:
            try:
                imagen = base64.b64decode(imagen)
            except Exception:
                pass
        
        return Producto(
            codigo=data.get('codigo'),
            descripcion=data.get('descripcion'),
            precio=Decimal(str(data.get('precio', 0))),
            existencias=data.get('existencias', 0),
            unidad_fk=data.get('unidad_fk'),
            estatus=data.get('estatus', 1),
            imagen_producto_ruta= imagen
        )