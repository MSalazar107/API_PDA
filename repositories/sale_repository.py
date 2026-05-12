from mysql.connector import Error
import datetime

class SaleRepository:
    """
    Repositorio para gestionar las transacciones de ventas en MySQL.
    
    Esquema de referencia para Swagger (Representación en BD):
    ---
    definitions:
      TicketBD:
        type: object
        properties:
          Folio:
            type: string
            description: Folio de la venta generado automáticamente basado en la fecha y hora.
            example: "20260512143000"
          fecha:
            type: string
            format: date-time
            description: Fecha y hora exacta de la transacción.
            example: "2026-05-12 14:30:00"
          numero_de_caja:
            type: integer
            description: ID de la caja donde se realizó la venta.
            example: 1
          total_venta:
            type: number
            format: float
            description: Monto total de la transacción.
            example: 850.50
    """
    def __init__(self, db):
        self.db = db
    
    def registrar_transaccion(self, venta):
        conn = self.db.connect()
        conn.autocommit = False 
        cur = conn.cursor()

        try:
            ahora = datetime.datetime.now()
            folio_id = ahora.strftime("%Y%m%d%H%M%S")
            venta.fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            
            
            cur.callproc('RegistrarCabeceraTicket', (
                folio_id, 
                venta.fecha, 
                venta.numero_caja, 
                float(venta.total)
            ))
            
            
            for detalle in venta.detalles:
                
                cur.callproc('RegistrarDetalleYRestarStock', (
                    folio_id, 
                    detalle.codigo_producto, 
                    detalle.cantidad, 
                    float(detalle.precio_unitario), 
                    float(detalle.importe)
                ))
            
            
            conn.commit()
            venta.folio = folio_id
            return True

        except Error as e:
            if conn:
                conn.rollback() 
            print(f"Error en la transacción: {e}")
            raise Exception(f"Error de base de datos: {str(e)}")
        finally:
            cur.close()
            conn.close()