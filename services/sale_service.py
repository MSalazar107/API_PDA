from models.venta import Venta, DetalleVenta
from decimal import Decimal

class SaleService:
    def __init__(self, sale_repository, product_repository):
        self.sale_repository = sale_repository
        self.product_repo = product_repository
        
    def procesar_venta(self, data, numero_caja):
        productos_solicitados = data.get('productos', [])
        
        if not numero_caja:
            raise ValueError("El número de caja es requerido.")
        if not productos_solicitados:
            raise ValueError("La lista de productos no puede estar vacía.")
        
        nueva_venta = Venta(numero_caja=numero_caja)
        actualizaciones_inventario = []

        for item in productos_solicitados:
            codigo = item.get('codigo')
            cantidad = int(item.get('cantidad', 0))
            
            if cantidad <= 0:
                raise ValueError(f"La cantidad para el producto {codigo} debe ser mayor a cero.")
            
            producto_bd = self.product_repo.get_by_id(codigo)
            
            if not producto_bd:
                raise ValueError(f"Producto con código '{codigo}' no encontrado en el sistema.")
        
            if cantidad > producto_bd["existencias"]:
                raise ValueError(f"Stock insuficiente para '{producto_bd['descripcion']}'. Disponible: {producto_bd['existencias']}")
            
            if producto_bd['estatus'] == 0:
                raise ValueError(f"El producto '{producto_bd['descripcion']}' no está disponible para venta.")
            
            precio = Decimal(str(producto_bd["precio"]))
            importe = precio * Decimal(str(cantidad))
        
            detalle = DetalleVenta(
                codigo_producto=codigo,
                nombre_producto=producto_bd["descripcion"], 
                cantidad=cantidad, 
                precio_unitario=precio, 
                importe=importe
            )
            nueva_venta.detalles.append(detalle)

            nueva_existencia = producto_bd["existencias"] - cantidad
            actualizaciones_inventario.append((codigo, nueva_existencia))
        
        nueva_venta.calcular_total()
        
        id_venta_generado = self.sale_repository.registrar_transaccion(nueva_venta)
        
        if id_venta_generado:
            for codigo_prod, nuevo_stock in actualizaciones_inventario:
                self.product_repo.update_stock(codigo_prod, nuevo_stock)
        else:
            raise Exception("No se pudo completar el registro de la venta en la base de datos.")

        return nueva_venta.to_dict()