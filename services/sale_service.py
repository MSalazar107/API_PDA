from models.venta import Venta, DetalleVenta
from decimal import Decimal

class SaleService:
    def __init__(self, sale_repository,product_repository):
        self.sale_repository = sale_repository
        self.product_repo = product_repository
        
    def procesar_venta(self, data, numero_caja):
        productos_solicitados = data.get('productos', [])
        
        if not numero_caja:
            raise ValueError("El número de caja es requerido.")
        if not productos_solicitados:
            raise ValueError("La lista de productos no puede estar vacía.")
        
        nueva_venta = Venta(numero_caja=numero_caja)
        
        for item in productos_solicitados:
            codigo = item.get('codigo')
            cantidad = item.get('cantidad')
            
            if cantidad <= 0:
                raise ValueError(f"La cantidad para el producto {codigo} debe ser mayor a cero.")
            
            producto_bd = self.product_repo.get_by_id(codigo)
            if not producto_bd:
             raise ValueError(f"Producto con código {codigo} no encontrado.")
        
            if cantidad > producto_bd["existencias"]:
                raise ValueError(f"Stock insuficiente para '{producto_bd['descripcion']}'.")
            
            if producto_bd ['estatus'] == 0:
                raise ValueError(f"El producto '{producto_bd['descripcion']}' no esta disponible.")
            
            precio = Decimal(str(producto_bd["precio"]))
            importe = precio * Decimal(str(cantidad))
        
            detalle = DetalleVenta(codigo, cantidad = cantidad, precio_unitario=precio, importe=importe)
            nueva_venta.detalles.append(detalle)
        
        nueva_venta.calcular_total()
        
        self.sale_repository.registrar_transaccion(nueva_venta)
        return nueva_venta.to_dict()