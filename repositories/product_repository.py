from mysql.connector import Error
from models.product import Producto

class ProductRepository:
    def __init__(self, db):
        self.db = db

   

    def create(self, p):
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            
            
            params = (
                p['codigo'], 
                p['descripcion'], 
                p['precio'], 
                p['existencias'], 
                p['unidad_fk'], 
                p['imagen_producto_ruta']
            )
            
            print("Llamando al Procedure InsertarProducto con:", p['codigo'])
            
            
            cur.callproc('InsertarProducto', params)
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
            

            cur.callproc('ActualizarExistencia', (codigo, nueva_existencia))
            conn.commit()
            
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def delete_logic(self, codigo):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            
            cur.callproc('DarDeBajaProducto', (codigo,))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()
    
    
    def update(self, codigo, p):
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            
           
            params = (
                codigo, 
                p['descripcion'], 
                p['precio'], 
                p['existencias'], 
                p['unidad_fk'], 
                p['imagen_producto_ruta']
            )
            
            # Llamamos al procedimiento almacenado
            cur.callproc('EditarProducto', params)
            conn.commit()
            
            return True 
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
       
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            
            
            cur.execute("SELECT ObtenerStockDisponible(%s) AS stock_actual", (codigo,))
            resultado = cur.fetchone()
            
            return resultado['stock_actual'] if resultado else 0
        finally:
            cur.close()
            conn.close()
            
    def agregar_inventario(self, codigo, cantidad_nueva):
        
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            
            # Llamamos al procedimiento y le pasamos los 2 parámetros
            cur.callproc('AgregarStock', (codigo, cantidad_nueva))
            conn.commit()
            
            return True
        except Error as e:
            print(f"Error al agregar stock: {e}")
            return False
        finally:
            cur.close()
            conn.close()