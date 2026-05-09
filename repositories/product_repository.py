from mysql.connector import Error

class ProductRepository:
    def __init__(self, db):
        self.db = db

    # --- OPERACIONES DE PRODUCTOS ---

    def create(self, p):
        """Inserta un nuevo producto en la tabla PRODUCTO"""
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = """
                INSERT INTO PRODUCTO (codigo, descripcion, precio, existencias, estatus, unidad_fk, imagen_producto_ruta)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # El estatus se manda como 1 (activo) por defecto
            params = (p['codigo'], p['descripcion'], p['precio'], p['existencias'], 1, p['unidad_fk'], p['imagen_producto_ruta'])
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
        """Obtiene todos los productos con el nombre de su unidad"""
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            # Usamos un JOIN para traer la descripción de la unidad de una vez
            query = """
                SELECT p.*, u.descripcionUnidad 
                FROM PRODUCTO p
                JOIN CATLG_UNITS u ON p.unidad_fk = u.ID_unidad
                WHERE p.estatus = 1
            """
            cur.execute(query)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def get_by_codigo(self, codigo):
        """Busca un producto específico por su llave primaria"""
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
        """Actualiza solo las existencias (útil para el módulo de ventas)"""
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
        """Borrado lógico: cambia estatus a 0 para no perder historial de ventas"""
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

    # --- OPERACIONES DE CATÁLOGO (UNIDADES) ---

    def get_units(self):
        """Lista las unidades disponibles para llenar selects en el frontend"""
        try:
            conn = self.db.connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM CATLG_UNITS")
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()