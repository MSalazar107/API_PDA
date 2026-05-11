from mysql.connector import Error
import datetime

class SaleRepository:
    def _init_(self, db):
        self.db = db
    
    def registrar_transaccion(self, venta):
        conn = self.db.get_connection()
        conn.autocommit = False
        cur = conn.cursor()

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
                float(venta.total)
            ))
            
            query_detalle = """
                INSERT INTO TICKET_DETALLE (Folio_ticket, Codigo_Producto, Cantidad, precio_unitario, importe) 
                VALUES (%s, %s, %s, %s, %s)
            """
            query_stock = "UPDATE PRODUCTO SET existencias = existencias - %s WHERE codigo = %s"
            
            for detalle in venta.detalles:
                cur.execute(query_detalle, (
                    folio_id, 
                    detalle.codigo_producto, 
                    detalle.cantidad, 
                    float(detalle.precio_unitario), 
                    float(detalle.importe)
                ))
                
                cur.execute(query_stock, (detalle.cantidad, detalle.codigo_producto))
            
            conn.commit()
            venta.folio = folio_id
            return True

        except Error as e:
            if conn:
                conn.rollback()
            raise Exception(f"Error de base de datos: {str(e)}")
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()