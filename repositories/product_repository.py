from mysql.connector import Error
from models.product import Producto

class ProductRepository:
    def __init__(self, db):
        self.db = db

   

    def create(self, p):
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = """
                INSERT INTO PRODUCTO (codigo, descripcion, precio, existencias, estatus, unidad_fk, imagen_producto_ruta)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            #
            params = (p['codigo'], p['descripcion'], p['precio'], p['existencias'], 1, p['unidad_fk'], p['imagen_producto_ruta'])
            print("VALORES QUE LLEGAN AL REPO:", params)
            cur.execute(query, params)
            conn.commit()
            return True
        except Error as e:
            print(f"Error al crear producto: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def get_all(self):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
         
            query = """
                SELECT * FROM Vista_Productos_Activos
            """
            cur.execute(query)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def get_by_id(self, codigo):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            query = "SELECT * FROM PRODUCTO WHERE codigo = %s"
            cur.execute(query, (codigo,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def update_stock(self, codigo, nueva_existencia):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = "UPDATE PRODUCTO SET existencias = %s WHERE codigo = %s"
            cur.execute(query, (nueva_existencia, codigo))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    def delete_logic(self, codigo):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = "UPDATE PRODUCTO SET estatus = 0 WHERE codigo = %s"
            cur.execute(query, (codigo,))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()
    
    
    def update(self, codigo, p):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = """
                UPDATE PRODUCTO 
                SET descripcion = %s, precio = %s, existencias = %s, 
                    unidad_fk = %s, imagen_producto_ruta = %s
                WHERE codigo = %s
            """
            params = (p['descripcion'], p['precio'], p['existencias'], p['unidad_fk'], p['imagen_producto_ruta'], codigo)
            cur.execute(query, params)
            conn.commit()
            return cur.rowcount > 0 
        except Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            cur.close()
            conn.close()



    def get_units(self):
    
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM CATLG_UNITS")
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
            
    def consultar_stock_bd(self, codigo):
        """Llama a la función de MySQL para ver cuánto stock real queda"""
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            
            
            cur.execute("SELECT ObtenerStockDisponible(%s) AS stock_actual", (codigo,))
            resultado = cur.fetchone()
            
            return resultado['stock_actual'] if resultado else 0
        finally:
            cur.close()
            conn.close()