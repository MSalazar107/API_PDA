from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal

def clean_num(value):
    if isinstance(value,(tuple,list)):
        return value[0]
    return value

@dataclass
class DetalleVenta:
    
    codigo_producto: str
    nombre_producto: str
    cantidad: int
    precio_unitario: Decimal = Decimal('0.00')
    importe: Decimal = Decimal('0.00')
    
    def to_dict(self):
        return {
            "codigo_producto": self.codigo_producto,
            "nombre_producto": self.nombre_producto,    
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "importe": float(self.importe)
        }
        
@dataclass
class Venta:
    numero_caja: int
    detalles: List[DetalleVenta] = field(default_factory=list)
    folio: Optional[int] = None
    fecha: Optional[str] = None
    total: Decimal = Decimal('0.00')
    
    def calcular_total(self):
        self.total = sum(Decimal(str(clean_num(detalle.importe))) for detalle in self.detalles)
        
    def to_dict(self):
        return {
            "folio": self.folio,
            "fecha": self.fecha,
            "numero_caja": self.numero_caja,
            "total": float(self.total),
            "detalles": [detalle.to_dict() for detalle in self.detalles]
        }
        