from decimal import Decimal
from mysql.connector import Error
import datetime

class SaleRepository:
    def __init__(self, db):
        self.db = db
    
    def registrar_transaccion(self, venta):
        conn = self.db.connect()
        conn.autocommit = False
        cur = conn.cursor()

        def f(val):
            if isinstance(val, (tuple, list)):
                val = val[0]
            try:
                return float(val) if val is not None else 0.0
            except:
                return 0.0

        try:
            ahora = datetime.datetime.now()
            folio_id = ahora.strftime("%Y%m%d%H%M%S")
            venta.fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            
            query_ticket = """
                INSERT INTO TICKET (Folio, fecha, numero_de_caja, total_venta) 
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(query_ticket, (
                folio_id, 
                venta.fecha, 
                venta.numero_caja, 
                f(venta.total)
            ))
            
            query_detalle = """
                INSERT INTO TICKET_DETALLE (Folio_ticket, Codigo_Producto, Cantidad, precio_unitario, importe) 
                VALUES (%s, %s, %s, %s, %s)
            """
            query_stock = "UPDATE PRODUCTO SET existencias = existencias - %s WHERE codigo = %s"
            
            for detalle in venta.detalles:
                p_u = f(detalle.precio_unitario)
                subtotal = f(detalle.importe)
                
                cur.execute(query_detalle, (
                    folio_id, 
                    detalle.codigo_producto, 
                    detalle.cantidad, 
                    p_u, 
                    subtotal
                ))
                
                cur.execute(query_stock, (detalle.cantidad, detalle.codigo_producto))
            
            conn.commit()
            venta.folio = folio_id
            return True

        except Error as e:
            conn.rollback()
            raise Exception(f"Error de base de datos: {str(e)}")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()